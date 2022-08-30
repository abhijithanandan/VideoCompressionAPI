import time
import psycopg2

from fastapi import FastAPI, status, HTTPException
from psycopg2.extras import RealDictCursor
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.database import engine, get_db

"""
Setup
"""

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


"""
Middleware
"""

try:
    conn = psycopg2.connect(host='localhost', database='VCApi', user='postgres', password='postgres',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Connection to database failed")
    print("Error: ", error)
    time.sleep(2)

"""
Routes
"""


@app.get("/users")
async def get_all_users(db: Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM public.users """)
    # users = cursor.fetchall()

    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no users found on the system")
    return {"data": users}


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # cursor.execute("""INSERT INTO public.users (name) VALUES (%s) RETURNING * """, user.name)
    # new_user = cursor.fetchone()
    # conn.commit()

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data": new_user}


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM public.users WHERE id =%s RETURNING *""", (str(id),))
    # deleted_user = cursor.fetchone()

    deleted_user = db.query(models.User).filter(models.User.id ==id)

    if deleted_user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    deleted_user.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


@app.put("users/{id}")
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

    return {"data": updated_user.first()}
