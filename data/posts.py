from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('Users', backref='posts')
    created_at = Column(DateTime, default=datetime.utcnow)
    text = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    views = Column(Integer, default=1)
    likes = relationship('Likes', backref='post')
