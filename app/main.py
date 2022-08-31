import time
import psycopg2

from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine
from app.routers import user, video, auth

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

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(video.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
