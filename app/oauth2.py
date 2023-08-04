from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.schemas import TokenDate

from . import models
from .config import settings
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.DB_SECRET_KEY
ALGORITHM = settings.DB_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.DB_ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data_in: dict):
    data_to_encode = data_in.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_expiration) -> TokenDate:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if not id:
            raise credentials_expiration
        token_data: TokenDate = TokenDate(id=id)

    except JWTError:
        raise credentials_expiration

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_expiration = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="not valid credentials",
        headers={"WWW-authenticate": "Bearer"},
    )

    token: TokenDate = verify_access_token(token, credentials_expiration)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
