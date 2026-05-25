from flask import Blueprint, abort, redirect, url_for, request
from flask_login import login_required, current_user
from data import db_session
from data.follows import Follows
from data.users import Users

follow_bp = Blueprint('follow', __name__)


@follow_bp.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    db_sess = db_session.create_session()
    try:
        if user_id == current_user.id:
            return redirect('/profile')

        user = db_sess.query(Users).filter_by(id=user_id).first()
        if not user:
            return abort(404)

        if not db_sess.query(Follows).filter_by(follower_id=current_user.id, followed_id=user_id).first():
            db_sess.add(Follows(follower_id=current_user.id, followed_id=user_id))
            db_sess.commit()

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        return redirect(url_for('profile.user_profile', username=user.username))

    finally:
        db_sess.close()


@follow_bp.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    db_sess = db_session.create_session()
    try:
        if user_id == current_user.id:
            return redirect('/profile')

        user = db_sess.query(Users).filter_by(id=user_id).first()
        if not user:
            return abort(404)

        follow = db_sess.query(Follows).filter_by(follower_id=current_user.id, followed_id=user_id).first()
        if follow:
            db_sess.delete(follow)
            db_sess.commit()

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        return redirect(url_for('profile.user_profile', username=user.username))

    finally:
        db_sess.close()
