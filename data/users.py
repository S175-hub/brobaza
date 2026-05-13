from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase
from data.follows import Follows


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    username = Column(String(20), nullable=True, unique=True)
    nickname = Column(String(30), nullable=True)
    description = Column(String(150), nullable=True)
    avatar = Column(String(100), nullable=True, default='avatars/default.jpg')
    registered_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    role = Column(String(20), default='user')
    verified = Column(Boolean, default=False)
    theme = Column(String(10), default='light')
    likes = relationship('Likes', backref='user', cascade='all, delete-orphan')
    followers = relationship('Follows', foreign_keys=[Follows.followed_id], backref='followed')
    following = relationship('Follows', foreign_keys=[Follows.follower_id], backref='follower')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
