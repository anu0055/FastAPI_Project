from fastapi import FastAPI, HTTPException, Response, Depends, APIRouter, status
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

@router.post("/", status_code=201)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post.id).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=409, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully add vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}
        
