import time
import psycopg2

from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

app = FastAPI()

"""
Models
"""


class User(BaseModel):
    id: int
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


@app.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    cursor.execute("""INSERT INTO users (name) VALUES (%s) RETURNING * """, user.name)
    new_user = cursor.fetchone()
    conn.commit()

    return {"data": new_user}