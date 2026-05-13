from sqlalchemy import Column, Integer, ForeignKey
from .db_session import SqlAlchemyBase


class Follows(SqlAlchemyBase):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    followed_id = Column(Integer, ForeignKey('users.id'))
