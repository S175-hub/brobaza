import os
import os.path
from flask import Blueprint, render_template, redirect, abort, request, current_app, url_for
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
                filename = f'{comment.id}.{file.filename.split(".")[-1].lower()}'
                file.save(f'static/comments/{filename}')
                comment.image = f'comments/{filename}'
            db_sess.commit()

        return redirect(url_for('post.post_view', post_id=post_id))

    finally:
        db_sess.close()


@comment_bp.route('/comment/delete/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    db_sess = db_session.create_session()

    try:
        comment = db_sess.query(Comments).filter(Comments.id == comment_id).first()

        if not comment:
            abort(404)

        if not (comment.author_id == current_user.id or current_user.role in ('admin', 'moderator')):
            abort(403)

        # Удаляем картинку комментария, если есть
        if comment.image:
            file_path = os.path.join(current_app.root_path, 'static', comment.image)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)  # Теперь os импортирован правильно
                except Exception:
                    pass

        db_sess.delete(comment)
        db_sess.commit()

        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)

        return redirect(request.referrer or url_for('feed.feed'))

    finally:
        db_sess.close()


@comment_bp.route('/comment/edit/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    db_sess = db_session.create_session()

    try:
        comment = db_sess.query(Comments).filter(Comments.id == comment_id).first()

        if not comment:
            abort(404)

        if comment.author_id != current_user.id:
            abort(403)

        form = AddComment()

        if form.validate_on_submit():
            text = (form.text.data or "").strip()
            file = form.image.data
            delete_image = 'delete_image' in request.form

            # Проверка на пустоту
            if not text and not (file and file.filename) and not (comment.image and not delete_image):
                form.text.errors.append('Комментарий не может быть пустым')
                return render_template('comment_edit.html', form=form, comment=comment)

            comment.text = text

            # Обработка новой картинки
            if file and file.filename:
                if comment.image:
                    old_path = os.path.join(current_app.root_path, 'static', comment.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                filename = f'{comment.id}.{file.filename.split(".")[-1].lower()}'
                file.save(f'static/comments/{filename}')
                comment.image = f'comments/{filename}'

            # Обработка удаления старой картинки
            elif delete_image:
                if comment.image:
                    old_path = os.path.join(current_app.root_path, 'static', comment.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                    comment.image = None

            db_sess.commit()

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)

            return redirect(url_for('post.post_view', post_id=comment.post_id))

        return render_template('comment_edit.html', form=form, comment=comment)

    finally:
        db_sess.close()