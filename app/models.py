from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    videos = relationship("Video")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String, default=f"Video uploaded for compression", nullable=False)
    url = Column(String, nullable=False)
    upload_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
