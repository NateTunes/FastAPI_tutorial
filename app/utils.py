from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"])


def hash(pwd: str):
    return pwd_ctx.hash(pwd)


def verify(password, hashed) -> bool:
    return pwd_ctx.verify(password, hashed)
