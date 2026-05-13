from sqlalchemy.orm import joinedload
from data.posts import Posts
from data.likes import Likes
from utils.date import time_ago


def get_profile_likes(db_sess, user_id):
    posts = (
        db_sess.query(Posts)
        .options(joinedload(Posts.author), joinedload(Posts.likes))
        .join(Likes, Likes.post_id == Posts.id)
        .filter(Likes.user_id == user_id)
        .order_by(Likes.id.desc())
        .all()
    )

    for post in posts:
        post.pretty_date = time_ago(post.created_at)
        post.like_count = len(post.likes)

    return posts


def get_posts(db_sess, user_id):
    posts = (
        db_sess.query(Posts)
        .options(joinedload(Posts.author), joinedload(Posts.likes))
        .filter(Posts.author_id == user_id)
        .order_by(Posts.created_at.desc())
        .all()
    )

    for post in posts:
        post.pretty_date = time_ago(post.created_at)
        post.like_count = len(post.likes)

    return posts


def get_liked_post_ids(db_sess, user_id):
    liked_post_ids = {
        row[0] for row in db_sess.query(Likes.post_id)
        .filter(Likes.user_id == user_id)
        .all()
    }

    return liked_post_ids
