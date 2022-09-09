import shutil
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Response, File, UploadFile, Form
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
    videos = db.query(models.Video).filter(models.Video.user_id == current_user.id,
                                           models.Video.title.contains(search)).limit(limit).offset(skip).all()
    return videos


@router.post("/videos", response_model=schemas.VideoResponse)
def upload_new_video(
        title: str = Form(),
        description: str = Form(),
        uri: str = Form(),
        file_uploaded: UploadFile = File(),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    destination = Path("temp_video_storage/" + str(file_uploaded.__hash__()) + "_" + file_uploaded.filename + ".mp4")
    new_video_meta = models.Video(user_id=current_user.id, **{
        "title": title,
        "description": description,
        "uri": uri,
        "name": file_uploaded.filename,
        "hash_name": destination.name
    })
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file_uploaded.file, buffer)
    finally:
        file_uploaded.file.close()
    db.add(new_video_meta)
    db.commit()
    db.refresh(new_video_meta)

    return new_video_meta


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
