import os
from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from data import db_session
from data.users import Users
from forms.profile_edit import ProfileEditForm

profile_edit_bp = Blueprint('profile_edit', __name__)


@profile_edit_bp.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileEditForm()

    db_sess = db_session.create_session()
    user = db_sess.query(Users).get(current_user.id)

    if form.validate_on_submit():
        if db_sess.query(Users).filter(Users.username == form.username.data, Users.id != current_user.id).first():
            form.username.errors.append('Имя пользователя занято')
            return render_template('profile_edit.html', form=form)

        user.username = form.username.data
        user.nickname = form.nickname.data
        user.description = form.description.data

        file = form.avatar.data
        if file and file.filename:
            ext = file.filename.rsplit('.', 1)[-1].lower()
            filename = f'{user.id}.{ext}'
            file.save(f'static/avatars/{filename}')
            user.avatar = f'avatars/{filename}'
        elif 'delete_avatar' in request.form:
            user.avatar = f'avatars/default.jpg'
            if user.avatar != 'avatars/default.jpg':
                old_path = os.path.join('static/avatars', user.avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)
            user.avatar = 'avatars/default.jpg'

        db_sess.commit()
        return redirect('/profile')

    form.username.data = user.username
    form.nickname.data = user.nickname
    form.description.data = user.description

    return render_template('profile_edit.html', form=form)
