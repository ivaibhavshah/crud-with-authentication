import hashlib
import json
import os
import random
import secrets
from datetime import datetime, timedelta
from uuid import uuid4

import bcrypt
from fastapi import HTTPException, status
from jwcrypto import jwk, jwt

from app.config import JWT_KEY


def now():
    return datetime.now()


def generate_id():
    return str(uuid4())


def generate_key():
    return uuid4().hex


def create_hash(key: str) -> str:
    key = key.encode()
    key = hashlib.sha256(key).digest()
    key = key.decode("unicode_escape")
    return key


def create_password(password: str) -> str:
    password = password.encode("utf-8")
    password = bcrypt.hashpw(password, bcrypt.gensalt(4))
    password = password.decode("utf-8")
    return password
