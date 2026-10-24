import os
from dotenv import load_dotenv
import jwt

from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS =  int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise RuntimeError("Неверный ключ!")


if ALGORITHM != "HS256":
    raise RuntimeError("Неверный алгоритм хеширования!")


if ACCESS_TOKEN_EXPIRE_MINUTES <= 0 or REFRESH_TOKEN_EXPIRE_DAYS <= 0:
    raise RuntimeError("Токены недействительны!")

password_hash = PasswordHash.recommended()



def create_access_token(user_id: int, role_id: int):
    now = datetime.now(timezone.utc)
    expiries_at = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "role_id": role_id,
        "type": "access",
        "iat": now,
        "exp": expiries_at
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, expiries_at


def create_refresh_token(user_id: int, role_id: int):
    now = datetime.now(timezone.utc)
    expiries_at = now + timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": expiries_at
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, expiries_at


def decode_token(token: str, expected_type: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=(ALGORITHM), options = {"requare": ["sub", 'type', 'iat', 'exp']})

    if payload['type'] != expected_type:
        raise jwt.InvalidTokenError("Неверный тип токена")
    
    return payload


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)
