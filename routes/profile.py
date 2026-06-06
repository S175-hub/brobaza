from flask import Blueprint, abort, render_template, redirect
from flask_login import login_required, current_user
from data import db_session
from data.follows import Follows
from data.users import Users
from utils.date import register_date
from utils.profile import get_posts, get_profile_likes, get_followers, get_following, get_following_ids

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
@login_required
def profile():
    db_sess = db_session.create_session()
    try:
        user = db_sess.get(Users, current_user.id)
        posts = get_posts(db_sess, user.id, current_user.id)
        registered_on = register_date(user.registered_on)
        followed = db_sess.query(Follows).filter_by(follower_id=user.id).count()
        followers = db_sess.query(Follows).filter_by(followed_id=user.id).count()

        return render_template('profile.html', user=user, posts=posts, active_tab='posts', registered_on=registered_on,
                               followed=followed, followers=followers)
    finally:
        db_sess.close()


@profile_bp.route('/<username>')
def user_profile(username):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(Users).filter(Users.username == username).first()

        if not user:
            abort(404)

        current_user_id = current_user.id if current_user.is_authenticated else None

        posts = get_posts(db_sess, user.id, current_user_id)
        registered_on = register_date(user.registered_on)
        followed = db_sess.query(Follows).filter_by(follower_id=user.id).count()
        followers = db_sess.query(Follows).filter_by(followed_id=user.id).count()

        if not current_user.is_authenticated:
            return render_template('profile.html', user=user, posts=posts, active_tab='posts',
                                   registered_on=registered_on, followed=followed, followers=followers,
                                   is_following=False)

        if user.id != current_user.id:
            is_following = True if db_sess.query(Follows).filter_by(follower_id=current_user.id,
                                                                    followed_id=user.id).first() else False
            return render_template('profile.html', user=user, posts=posts, active_tab='posts',
                                   registered_on=registered_on, followed=followed, followers=followers,
                                   is_following=is_following)

        return redirect('/profile')

    finally:
        db_sess.close()


@profile_bp.route('/profile/likes')
@login_required
def profile_likes():
    db_sess = db_session.create_session()
    try:
        user = db_sess.get(Users, current_user.id)
        posts = get_profile_likes(db_sess, user.id, current_user.id)
        registered_on = register_date(user.registered_on)
        followed = db_sess.query(Follows).filter_by(follower_id=user.id).count()
        followers = db_sess.query(Follows).filter_by(followed_id=user.id).count()

        return render_template('profile.html', user=user, posts=posts, active_tab='likes', registered_on=registered_on,
                               followed=followed, followers=followers)
    finally:
        db_sess.close()


@profile_bp.route('/profile/following')
@login_required
def following():
    db_sess = db_session.create_session()
    try:
        user = db_sess.get(Users, current_user.id)
        following = get_following(db_sess, user.id)
        return render_template('follows.html', user=user, active_tab='following', following=following)
    finally:
        db_sess.close()


@profile_bp.route('/profile/followers')
@login_required
def followers():
    db_sess = db_session.create_session()
    try:
        user = db_sess.get(Users, current_user.id)
        followers = get_followers(db_sess, user.id)
        following_ids = get_following_ids(db_sess, user.id)
        return render_template('follows.html', user=user, active_tab='followers', followers=followers,
                               following_ids=following_ids)
    finally:
        db_sess.close()


@profile_bp.route('/<username>/following')
def user_following(username):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(Users).filter(Users.username == username).first()

        if not user:
            abort(404)

        following = get_following(db_sess, user.id)
        following_ids = get_following_ids(db_sess, current_user.id) if current_user.is_authenticated else set()
        if not (current_user.is_authenticated and user.id == current_user.id):
            return render_template('follows.html', user=user, active_tab='following', following=following,
                                   following_ids=following_ids)

        return redirect('/profile/following')

    finally:
        db_sess.close()


@profile_bp.route('/<username>/followers')
def user_followers(username):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(Users).filter(Users.username == username).first()

        if not user:
            abort(404)

        followers = get_followers(db_sess, user.id)
        following_ids = get_following_ids(db_sess, current_user.id) if current_user.is_authenticated else set()
        if not (current_user.is_authenticated and user.id == current_user.id):
            return render_template('follows.html', user=user, active_tab='followers', followers=followers,
                                   following_ids=following_ids)

        return redirect('/profile/followers')

    finally:
        db_sess.close()
