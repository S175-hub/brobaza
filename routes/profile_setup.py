from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from data import db_session
from data.users import Users
from forms.profile_setup import ProfileSetupForm

profile_setup_bp = Blueprint('profile_setup', __name__)


@profile_setup_bp.route('/profile_setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    form = ProfileSetupForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if db_sess.query(Users).filter(Users.username == form.username.data, Users.id != current_user.id).first():
            form.username.errors.append('Имя пользователя занято')
            return render_template('profile_setup.html', form=form)

        user = db_sess.query(Users).get(current_user.id)
        user.username = form.username.data
        user.nickname = form.nickname.data
        user.description = form.description.data

        file = form.avatar.data
        if file and file.filename:
            filename = f'{user.id}.{file.filename.split('.')[-1].lower()}'
            file.save(f'static/avatars/{filename}')
            user.avatar = f'avatars/{filename}'
        else:
            user.avatar = 'avatars/default.jpg'
        db_sess.commit()

        return redirect('/')

    return render_template('profile_setup.html', form=form)
