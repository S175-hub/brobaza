from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from data import db_session
from data.likes import Likes

like_bp = Blueprint('like', __name__)


@like_bp.route('/like/<int:post_id>')
@login_required
def like(post_id):
    db_sess = db_session.create_session()

    try:
        like = db_sess.query(Likes).filter(Likes.user_id == current_user.id, Likes.post_id == post_id).first()
        if like:
            db_sess.delete(like)
            liked = False
        else:
            db_sess.add(Likes(user_id=current_user.id, post_id=post_id))
            liked = True

        db_sess.commit()
        count = db_sess.query(Likes).filter(Likes.post_id == post_id).count()

        return jsonify({"liked": liked, "count": count})

    finally:
        db_sess.close()
