from .database import Base  
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, PrimaryKeyConstraint
from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "Posts"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post") 

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    posts = relationship("Post", back_populates="owner")
    likes = relationship("Like", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")  # 👈 add this
    replies = relationship("Reply", back_populates="owner")

class Like(Base):
    __tablename__ = "Likes"
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("Posts.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "post_id"),
    )

    owner = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes") 

class Comment(Base):
    __tablename__ = "Comments"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    post_id = Column(Integer, ForeignKey("Posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    post = relationship("Post", back_populates="comments")
    owner = relationship("User", back_populates="comments")
    replies = relationship("Reply", back_populates="comment")

class Reply(Base):
    __tablename__ = "Replies"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    comment_id = Column(Integer, ForeignKey("Comments.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    comment = relationship("Comment", back_populates="replies")
    owner = relationship("User", back_populates="replies")