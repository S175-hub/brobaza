from flask import Blueprint, request, redirect, render_template, url_for, abort
from flask_login import login_required, current_user
from data import db_session
from data.posts import Posts
from data.comments import Comments
from forms.add_comment import AddComment

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    form = AddComment()

    db_sess = db_session.create_session()

    try:
        post = db_sess.query(Posts).filter(Posts.id == post_id).first()

        if not post:
            abort(404)

        if form.validate_on_submit():
            text = form.text.data
            file = form.image.data

            if not text and (not file or not file.filename):
                form.text.errors.append('Комментарий не может быть пустым')
                return redirect(url_for('post.post_view', post_id=post_id))

            comment = Comments(
                author_id=current_user.id,
                post_id=post_id,
                text=text
            )
            db_sess.add(comment)
            db_sess.flush()

            if file and file.filename:
                filename = f'{comment.id}.{file.filename.split('.')[-1].lower()}'
                file.save(f'static/comments/{filename}')
                comment.image = f'comments/{filename}'
            db_sess.commit()

        return redirect(url_for('post.post_view', post_id=post_id))

    finally:
        db_sess.close()
