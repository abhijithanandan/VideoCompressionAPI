from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette import status

from app import oauth2, models, schemas
from app.database import get_db

router = APIRouter()


@router.get("/videos")
def get_all_videos(db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user),
                   limit: int = 10,
                   skip: int = 0,
                   search: Optional[str] = ""):
    videos = db.query(models.Video).filter(models.Video.user_id == current_user.id, models.Video.title.contains(search)).limit(limit).offset(skip).all()
    return videos


@router.post("/videos", response_model=schemas.VideoResponse)
def upload_new_video(video: schemas.VideoBase, db: Session = Depends(get_db),
                     current_user: models.User = Depends(oauth2.get_current_user)):
    new_video = models.Video(user_id=current_user.id, **video.dict())
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return new_video


@router.delete("/videos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    video_to_delete = db.query(models.Video).filter(models.Video.id == id)

    if video_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"video with id {id} does not exist")

    if video_to_delete.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    video_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
