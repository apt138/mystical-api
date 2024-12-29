import os
from datetime import datetime, timezone, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from model.user import User
from data import user as db
from errors import InvalidUser

ph = PasswordHasher()
token_expiry_mintues: int = os.getenv("TOKEN_EXPIRATION_TIME_MINTUES", 15)
algorithm: str = "HS256"


# <--- CRUD --->
def get_all() -> list[User]:
    return db.get_all()


def get_one(name: str) -> User:
    return db.get_one(name)


def create(user: User) -> User:
    return db.create(user)


def replace(name: str, user: User) -> User:
    return db.replace(name, user)


def delete(name: str) -> None:
    return db.delete(name)


# <--- AUTH --->
def hash_password(pwd: str):
    return ph.hash(pwd)


def verify_password(hash_: str, pwd: str):
    try:
        ph.verify(hash_, pwd)
    except VerifyMismatchError:
        raise InvalidUser("Invalid user credentials")


def create_access_token(name: str):
    payload: dict[str, str] = {
        "sub": name,
        "exp": datetime.now(timedelta.utc) + timedelta(minutes=token_expiry_mintues),
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm=algorithm)
    return token


def lookup_user(name: str) -> User:
    return db.get_one(name)


def auth_user(name: str, pwd: str) -> User:
    user = lookup_user(name)
    verify_password(user.hash_, pwd)
    return user


def validate_user_token(token: str) -> User:
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[algorithm])
        exp = payload.get("exp")
        if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
            raise InvalidUser("Token expired")
        user = lookup_user(payload.get("sub"))
        return user
    except jwt.exceptions.PyJWTError:
        raise InvalidUser("Invalid token")
