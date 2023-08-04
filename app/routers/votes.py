from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)  # , response_model=schemas.Vote)
async def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    # check if post exist
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {vote.post_id} does not exist",
        )

    # query the vote
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == curr_user.id
    )

    existing_vote = vote_query.first()
    # if vote up
    if vote.direction == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"user {curr_user} already vote for this post",
            )

        new_vote = models.Votes(post_id=vote.post_id, user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"details": "vote up!"}
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user do not have vote for this post",
            )

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"details": "vote down"}
