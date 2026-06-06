from flask import Blueprint, render_template
from flask_login import current_user
from data import db_session
from forms.add_post import AddPost
from utils.feed import get_feed

feed_bp = Blueprint('feed', __name__)


@feed_bp.route('/feed')
def feed():
    form = AddPost()

    db_sess = db_session.create_session()
    posts = get_feed(db_sess, current_user)
    return render_template('feed.html', form=form, posts=posts)
