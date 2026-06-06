from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from data import db_session
from data.posts import Posts
from forms.add_post import AddPost
from ui.emojis import EMOJI_LIST
from utils.feed import get_feed

create_bp = Blueprint('create', __name__)


@create_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = AddPost()

    db_sess = db_session.create_session()
    posts = get_feed(db_sess, current_user)

    if form.validate_on_submit():
        text = form.text.data
        file = form.image.data

        if not text and (not file or not file.filename):
            form.text.errors.append('Пост не может быть пустым')
            return render_template('feed.html', form=form, posts=posts)

        post = Posts(
            author_id=current_user.id,
            text=text
        )
        db_sess.add(post)
        db_sess.flush()

        if file and file.filename:
            filename = f'{post.id}.{file.filename.split('.')[-1].lower()}'
            file.save(f'static/posts/{filename}')
            post.image = f'posts/{filename}'
        db_sess.commit()

        return redirect('/feed')

    return render_template('feed.html', form=form, posts=posts)
