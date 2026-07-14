from data.posts import Posts
from data.likes import Likes
from data.comments import Comments
from utils.date import time_ago


def get_feed(db_sess, current_user):
    posts = (
        db_sess.query(Posts)
        .order_by(Posts.created_at.desc())
        .all()
    )

    liked_post_ids = {
        row[0] for row in db_sess.query(Likes.post_id)
        .filter(Likes.user_id == current_user.id)
        .all()
    } if current_user.is_authenticated else set()

    reposted_post_ids = {
        row[0] for row in db_sess.query(Posts.repost_post_id)
        .filter(Posts.author_id == current_user.id, Posts.repost_post_id.isnot(None))
        .all()
    } if current_user.is_authenticated else set()

    for post in posts:
        post.pretty_date = time_ago(post.created_at)
        post.like_count = len(post.likes)
        post.is_liked = post.id in liked_post_ids
        post.is_reposted = post.id in reposted_post_ids
        post.comment_count = db_sess.query(Comments.id).filter(Comments.post_id == post.id).count()
        post.repost_count = db_sess.query(Posts.id).filter(Posts.repost_post_id == post.id).count()

    return posts


def get_post(db_sess, post_id, current_user):
    post = db_sess.get(Posts, post_id)

    post.pretty_date = time_ago(post.created_at)
    post.like_count = len(post.likes)
    post.comment_count = db_sess.query(Comments.id).filter(Comments.post_id == post.id).count()
    post.repost_count = db_sess.query(Posts.id).filter(Posts.repost_post_id == post.id).count()

    post.is_reposted = False
    if current_user.is_authenticated:
        is_reposted = db_sess.query(Posts.id).filter(
            Posts.author_id == current_user.id,
            Posts.repost_post_id == post.id
        ).first()
        if is_reposted:
            post.is_reposted = True

    if post.repost_post_id and post.original_post:
        post.original_post.pretty_date = time_ago(post.original_post.created_at)

    post.is_liked = False
    if current_user.is_authenticated:
        is_liked = db_sess.query(Likes.post_id).filter(
            Likes.user_id == current_user.id,
            Likes.post_id == post.id
        ).first()

        if is_liked:
            post.is_liked = True

    return post
