from flask import Blueprint, jsonify
from flask_login import login_required
from data import db_session
from data.posts import Posts
from data.users import Users

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/statistics', methods=['GET'])
@login_required
def api_get_statistics():
    db_sess = db_session.create_session()
    count_users = db_sess.query(Users).count()
    count_posts = db_sess.query(Posts).count()
    last_registered = db_sess.query(Users).order_by(Users.registered_on.desc()).first()

    return jsonify(
        {
            "users": count_users,
            "posts": count_posts,
            "last_registered": last_registered.registered_on.isoformat() if last_registered and last_registered.registered_on else None,
        }
    )


@api_bp.route('/users', methods=['GET'])
@login_required
def api_get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()

    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "registered_on": user.registered_on.isoformat() if user.registered_on else None,
        }
        for user in users])


@api_bp.route('/posts', methods=['GET'])
@login_required
def api_get_posts():
    db_sess = db_session.create_session()
    posts = db_sess.query(Posts).all()

    return jsonify([
        {
            "id": post.id,
            "author": {
                "id": post.author_id,
                "username": post.author.username if post.author else None
            },
            "text": post.text,
            "image": post.image,
            "created_at": post.created_at.isoformat() if post.created_at else None,
        }
        for post in posts])
