from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        user.password = utils.hash(user.password)
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="could not create user"
        )

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):

    query = db.query(models.User).filter(models.User.id == id)
    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find user of id = {id}",
        )

    return query.first()
