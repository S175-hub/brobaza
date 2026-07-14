from flask import Blueprint, abort, render_template, redirect
from flask_login import login_required, current_user
from data import db_session
from data.posts import Posts
from forms.add_post import AddPost
from utils.date import time_ago

repost_bp = Blueprint('repost', __name__)


@repost_bp.route('/post/<int:post_id>/repost', methods=['GET', 'POST'])
@login_required
def repost(post_id):
    form = AddPost()

    db_sess = db_session.create_session()
    original_post = db_sess.get(Posts, post_id)
    if not original_post:
        abort(404)

    original_post.pretty_date = time_ago(original_post.created_at)
    
    if form.validate_on_submit():
        text = form.text.data
        file = form.image.data

        post = Posts(
            author_id=current_user.id,
            text=text,
            repost_post_id=post_id,
        )
        db_sess.add(post)
        db_sess.flush()

        if file and file.filename:
            filename = f'{post.id}.{file.filename.split('.')[-1].lower()}'
            file.save(f'static/posts/{filename}')
            post.image = f'posts/{filename}'
        db_sess.commit()

        return redirect('/feed')

    return render_template('add_repost.html', form=form, original_post=original_post)
