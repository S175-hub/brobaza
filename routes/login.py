from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, login_user, logout_user
from data import db_session
from data.users import Users
from forms.login import LoginForm

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            theme = request.cookies.get('user_theme')
            if theme and theme != user.theme:
                db_sess = db_session.create_session()
                user = db_sess.query(Users).get(user.id)
                if user:
                    user.theme = theme
                    db_sess.commit()
            return redirect('/')
        form.email.errors.append("Неверная почта или пароль")

    return render_template('login.html', form=form)


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
