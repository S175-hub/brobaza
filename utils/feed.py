from data.posts import Posts
from data.likes import Likes
from utils.date import time_ago


def get_feed(db_sess, current_user):
    posts = (
        db_sess.query(Posts)
        .order_by(Posts.created_at.desc())
        .all()
    )

    for post in posts:
        post.pretty_date = time_ago(post.created_at)
        post.like_count = len(post.likes)

    liked_post_ids = {
        row[0] for row in db_sess.query(Likes.post_id)
        .filter(Likes.user_id == current_user.id)
        .all()
    } if current_user.is_authenticated else set()

    return posts, liked_post_ids
