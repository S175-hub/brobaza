import os.path
from flask import Blueprint, render_template, redirect, abort, request, current_app, url_for
from flask_login import current_user, login_required
from data import db_session
from data.comments import Comments
from data.posts import Posts
from data.likes_comments import LikesComments
from forms.add_comment import AddComment
from forms.add_post import AddPost
from utils.feed import get_post
from utils.date import time_ago

post_bp = Blueprint('post', __name__)


@post_bp.route('/post/<int:post_id>')
def post_view(post_id):
    db_sess = db_session.create_session()

    try:
        post = get_post(db_sess, post_id, current_user)

        if not post:
            abort(404)

        post = [post]
        form = AddComment()

        comments = db_sess.query(Comments).filter(Comments.post_id == post_id).order_by(
            Comments.created_at.desc()).all()

        liked_comment_ids = set()
        if current_user.is_authenticated:
            liked_comment_ids = {
                row[0] for row in db_sess.query(LikesComments.comment_id)
                .filter(LikesComments.user_id == current_user.id)
                .all()
            }

        for comment in comments:
            comment.pretty_date = time_ago(comment.created_at)
            comment.like_count = db_sess.query(LikesComments.id).filter(
                LikesComments.comment_id == comment.id
            ).count()
            comment.is_liked = comment.id in liked_comment_ids

        return render_template('post_view.html', posts=post, comments=comments, form=form, post_id=post_id)

    finally:
        db_sess.close()


@post_bp.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_delete(post_id):
    db_sess = db_session.create_session()

    try:
        post = db_sess.query(Posts).filter(Posts.id == post_id).first()

        if not post:
            abort(404)

        if not (post.author_id == current_user.id or current_user.role in ('admin', 'moderator')):
            abort(403)

        if post.image:
            file_path = os.path.join(current_app.root_path, 'static', post.image)
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


@post_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    db_sess = db_session.create_session()

    try:
        post = db_sess.query(Posts).filter(Posts.id == post_id).first()

        if not post:
            abort(404)

        if post.author_id != current_user.id:
            abort(403)

        form = AddPost()

        if form.validate_on_submit():
            text = (form.text.data or "").strip()
            file = form.image.data
            delete_image = 'delete_image' in request.form

            will_have_image = (file and file.filename) or (post.image and not delete_image)

            if not text and not will_have_image:
                form.text.errors.append('Пост не может быть пустым')
                return render_template('post_edit.html', form=form, post=post)

            post.text = text

            if file and file.filename:
                if post.image:
                    old_path = os.path.join(current_app.root_path, 'static', post.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                filename = f'{post.id}.{file.filename.split(".")[-1].lower()}'
                file.save(f'static/posts/{filename}')
                post.image = f'posts/{filename}'

            elif delete_image:
                if post.image:
                    old_path = os.path.join(current_app.root_path, 'static', post.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                    post.image = None

            db_sess.commit()

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)

            return redirect(url_for('feed.feed'))

        return render_template('post_edit.html', form=form, post=post)

    finally:
        db_sess.close()
