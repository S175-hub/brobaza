from flask import Blueprint, render_template, redirect
from flask_login import login_user
from data import db_session
from data.users import Users
from forms.register import RegisterForm

register_bp = Blueprint('register', __name__)


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            form.email.errors.append('Адрес электронной почты уже используется')
            return render_template('register.html', form=form)

        user = Users(email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        login_user(user)

        return redirect('/profile_setup')

    return render_template('register.html', form=form)
