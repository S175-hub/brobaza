from sqlalchemy.orm import joinedload
from data.users import Users
from data.posts import Posts
from data.likes import Likes
from data.comments import Comments
from data.follows import Follows
from utils.date import time_ago


def get_profile_likes(db_sess, user_id, current_user_id):
    posts = (
        db_sess.query(Posts)
        .options(joinedload(Posts.author), joinedload(Posts.likes))
        .join(Likes, Likes.post_id == Posts.id)
        .filter(Likes.user_id == user_id)
        .order_by(Likes.id.desc())
        .all()
    )

    liked_post_ids = {
        row[0] for row in db_sess.query(Likes.post_id)
        .filter(Likes.user_id == current_user_id)
        .all()
    } if current_user_id else set()

    for post in posts:
        post.pretty_date = time_ago(post.created_at)
        post.like_count = len(post.likes)
        post.is_liked = post.id in liked_post_ids
        post.comment_count = db_sess.query(Comments.id).filter(Comments.post_id == post.id).count()

    return posts


def get_posts(db_sess, user_id, current_user_id):
    posts = (
        db_sess.query(Posts)
        .options(joinedload(Posts.author), joinedload(Posts.likes))
        .filter(Posts.author_id == user_id)
        .order_by(Posts.created_at.desc())
        .all()
    )

    liked_post_ids = {
        row[0] for row in db_sess.query(Likes.post_id)
        .filter(Likes.user_id == current_user_id)
        .all()
    } if current_user_id else set()

    for post in posts:
        post.pretty_date = time_ago(post.created_at)
        post.like_count = len(post.likes)
        post.is_liked = post.id in liked_post_ids
        post.comment_count = db_sess.query(Comments.id).filter(Comments.post_id == post.id).count()

    return posts


# def get_liked_post_ids(db_sess, user_id):
#     liked_post_ids = {
#         row[0] for row in db_sess.query(Likes.post_id)
#         .filter(Likes.user_id == user_id)
#         .all()
#     }
#
#     return liked_post_ids


def get_following(db_sess, user_id):
    following = (
        db_sess.query(Users)
        .join(Follows, Follows.followed_id == Users.id)
        .filter(Follows.follower_id == user_id)
        .all()
    )
    return following


def get_followers(db_sess, user_id):
    followers = (
        db_sess.query(Users)
        .join(Follows, Follows.follower_id == Users.id)
        .filter(Follows.followed_id == user_id)
        .all()
    )
    return followers


def get_following_ids(db_sess, user_id):
    following_ids = {
        row[0] for row in db_sess.query(Follows.followed_id)
        .filter(Follows.follower_id == user_id)
        .all()
    }
    return following_ids
