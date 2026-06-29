from sqlalchemy import Column, Integer, ForeignKey
from .db_session import SqlAlchemyBase


class LikesComments(SqlAlchemyBase):
    __tablename__ = 'likes_comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
