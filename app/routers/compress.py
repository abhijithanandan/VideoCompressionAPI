import os.path
import shutil
import subprocess
import uuid
from pathlib import Path

from fastapi import APIRouter, Form, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(
    prefix="/compress",
    tags=["compress"]
)


@router.post("/", response_model=schemas.VideoResponse)
def compress_video(
        title: str = Form(),
        description: str = Form(),
        uri: str = Form(),
        file_uploaded: UploadFile = File(),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)):
    fid = uuid.uuid4()
    input_path = Path("temp_video_storage/" + str(fid) + "_" + file_uploaded.filename)
    output_path = Path("temp_output_storage/" + str(fid) + "_" + file_uploaded.filename)
    new_video_meta = models.Video(user_id=current_user.id, **{
        "title": title,
        "description": description,
        "uri": uri,
        "name": file_uploaded.filename,
        "hash_name": input_path.name
    })
    try:
        print(input_path)
        with open(input_path, 'wb') as buffer:
            shutil.copyfileobj(file_uploaded.file, buffer)
    finally:
        file_uploaded.file.close()
    db.add(new_video_meta)
    db.commit()
    db.refresh(new_video_meta)

    # handbrake_commands = [f"HandBrake/build/HandBrakeCLI", "-i", f"{input_path}", "-o", f"{output_path}", "-O"]
    handbrake_commands = [f"HandBrake/build/HandBrakeCLI -i {input_path} -o {output_path} -O"]

    if os.path.exists(input_path):
        subprocess.Popen(handbrake_commands, shell=True)
    else:
        print("File upload error")

    return new_video_meta


@router.get("/{file_name}")
async def download_video(file_name: str):
    output_path = Path("temp_output_storage/" + file_name)
    return FileResponse(output_path)
