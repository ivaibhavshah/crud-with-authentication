import json
import os

from fastapi import HTTPException, status

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
JWT_KEY = os.environ.get("JWT_KEY")

if JWT_KEY:
    try:
        JWT_KEY = json.loads(JWT_KEY)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT key"
        )
else:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWT key not set"
    )