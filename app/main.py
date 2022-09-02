from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import user, video, auth
from fastapi.middleware.cors import CORSMiddleware

"""
Setup
"""

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


"""
Middleware
"""
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
Routes
"""

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(video.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
