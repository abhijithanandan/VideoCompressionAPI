import time
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor

# SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ip-address/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = 'postgres://postgres:postgres@localhost/VCApi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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

