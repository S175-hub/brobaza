import os.path
from flask import Blueprint, redirect, abort, request
from flask_login import current_user, login_required
from data import db_session
from data.posts import Posts

post_bp = Blueprint('post', __name__)


@post_bp.route('/post/delete/<int:post_id>')
@login_required
def post_delete(post_id):
    db_sess = db_session.create_session()

    try:
        post = db_sess.query(Posts).filter(Posts.id == post_id).first()

        if not post:
            abort(404)

        if post.author_id != current_user.id:
            abort(403)

        if post.image:
            file_path = os.path.join('static', post.image)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

        db_sess.delete(post)
        db_sess.commit()

        next_page = request.args.get('next')

        if next_page and next_page.startswith('/'):
            return redirect(next_page)

        return redirect('/feed')

    finally:
        db_sess.close()
