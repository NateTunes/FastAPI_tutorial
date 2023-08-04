from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.oauth2 import create_access_token
from app.schemas import Token
from app.utils import verify

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model=Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    user: models.User = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user or not verify(user_credentials.password, user.password):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
        )

    token = create_access_token(data_in={"user_id": user.id})

    return Token(access_token=token, token_type="bearer")
