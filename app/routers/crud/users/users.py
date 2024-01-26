import json
import traceback
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException, status
from jwcrypto import jwk, jwt
from sqlalchemy.orm import Session

from app.config import JWT_KEY
from app.libs.utils import create_password, generate_id, now
from app.models import UserModel
from app.routers.schemas import Login, Signup


def get_token(user_id: str, email, exp_enable: bool):
    if exp_enable == True:
        expiration_time = datetime.now() + timedelta(minutes=1)
        print(expiration_time)
        exp_timestamp = int(expiration_time.timestamp())
        claims = {"id": user_id, "email": email, "exp": exp_timestamp}
    else:
        claims = {"id": user_id, "email": email, "time": str(now())}

    # Create a signed token with the generated key
    key = jwk.JWK(**JWT_KEY)
    token = jwt.JWT(header={"alg": "HS256"}, claims=claims)
    token.make_signed_token(key)

    # Further encription the token with same key
    encrypted_token = jwt.JWT(
        header={"alg": "A256KW", "enc": "A256CBC-HS512"}, claims=token.serialize()
    )
    encrypted_token.make_encrypted_token(key)
    return encrypted_token.serialize()


def verify_token(db: Session, token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Mising Token."
        )
    else:
        try:
            key = jwk.JWK(**JWT_KEY)
            ET = jwt.JWT(key=key, jwt=token, expected_type="JWE")
            ST = jwt.JWT(key=key, jwt=ET.claims)
            claims = ST.claims
            claims = json.loads(claims)
            db_user = get_user_by_id(id=claims["id"], db=db)

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        except jwt.JWTExpired as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired "
            )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found."
            )
        elif db_user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found."
            )
        return db_user


def get_user_by_id(id: str, db: Session):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.id == id, UserModel.is_deleted == False)
        .first()
    )
    return db_user


def get_user_by_email(db: Session, email: str):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.email == email, UserModel.is_deleted == False)
        .first()
    )
    return db_user


def sign_up(db: Session, signup: Signup):
    db_user = get_user_by_email(db, signup.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email Alredy Exist"
        )

    signup.password = create_password(signup.password)
    id = generate_id()
    db_user = UserModel(id=id, **signup.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


def login(login: Login, db: Session):
    db_user = get_user_by_email(email=login.email, db=db)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    hashed = db_user.password.encode("utf-8")
    password = login.password.encode("utf-8")

    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_user.token = get_token(db_user.id, db_user.email, exp_enable=True)
    return db_user


def get_profile(db: Session, token: str):
    db_user = verify_token(db, token=token)
    return db_user
