from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app import utils
from app import models
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[schemas.UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public.users """)
    # users = cursor.fetchall()

    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no users found on the system")
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO public.users (name) VALUES (%s) RETURNING * """, user.name)
    # new_user = cursor.fetchone()
    # conn.commit()

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM public.users WHERE id =%s RETURNING *""", (str(id),))
    # deleted_user = cursor.fetchone()

    deleted_user = db.query(models.User).filter(models.User.id == id)

    if deleted_user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    deleted_user.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UpdateUser, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE users SET name = %s WHERE id = %s RETURNING *""", (user.name, str(id)))
    # updated_user = cursor.fetchone()
    # conn.commit()

    updated_user = db.query(models.User).filter(models.User.id == id)

    if updated_user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    updated_user.update(user.dict(), synchronize_session=False)
    db.commit()

    return updated_user.first()
