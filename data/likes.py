from sqlalchemy import Column, Integer, ForeignKey
from .db_session import SqlAlchemyBase


class Likes(SqlAlchemyBase):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
