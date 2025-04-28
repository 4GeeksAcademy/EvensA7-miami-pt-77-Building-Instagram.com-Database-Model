from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

import enum

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list["Post"]] = db.relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = db.relationship("Comment", back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = db.relationship("User", backref="posts")
    comments: Mapped[list["Comment"]] = db.relationship("Comment", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    author: Mapped["User"] = db.relationship("User", backref="comments")
    post_id: Mapped[int] = mapped_column(db.ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = db.relationship("Post", backref="comments")
    comment_text: Mapped[str] = mapped_column(String(300), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "author_id": self.author.id
            # do not serialize the password, its a security breach
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(db.Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(300), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey("post.id"), nullable=False)
    post: Mapped["User"] = db.relationship("Post", backref="media")
    


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }