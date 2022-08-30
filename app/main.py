import time
import psycopg2

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db

"""
Setup
"""

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""
Models
"""


class User(BaseModel):
    id: int = 0
    name: str


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
async def get_all_users():
    cursor.execute(""" SELECT * FROM public.users """)
    users = cursor.fetchall()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no users found on the system")
    return users


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    cursor.execute("""INSERT INTO public.users (name) VALUES (%s) RETURNING * """, user.name)
    new_user = cursor.fetchone()
    conn.commit()

    return {"data": new_user}


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    cursor.execute("""DELETE FROM public.users WHERE id =%s RETURNING *""", (str(id),))
    deleted_user = cursor.fetchone()

    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    return status.HTTP_204_NO_CONTENT


@app.put("users/{id}")
def update_user(id: int, user: User):
    cursor.execute("""UPDATE users SET name = %s WHERE id = %s RETURNING *""", (user.name, str(id)))
    updated_user = cursor.fetchone()
    conn.commit()

    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"data": updated_user}
