from typing import Optional

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostsVotesResponse])
async def get_posts(
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    res = (
        db.query(models.Post, func.count(models.Votes.post_id).label("n_votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return res


@router.get(
    "/{id}",
    response_model=schemas.PostsVotesResponse,
)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post, func.count(models.Votes.post_id).label("n_votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post of id = {id}",
        )

    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=curr_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post of id = {id}",
        )

    if post_query.first().owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: int,
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post of id = {id}",
        )

    if post_query.first().owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
