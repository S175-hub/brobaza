from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import Length, Regexp, ValidationError
from flask_login import current_user


def custom_length_check(form, field):
    if current_user.is_authenticated and current_user.role == 'admin':
        if len(field.data) < 3:
            raise ValidationError('Username администратора может содержать от 3 до 20 символов')
    else:
        if len(field.data) < 5:
            raise ValidationError('Username пользователя может содержать от 5 символов')


class ProfileEditForm(FlaskForm):
    avatar = FileField('Аватар',
                       validators=[
                           FileAllowed(['jpg', 'png', 'jpeg'], message='Недопустимый формат файла')
                       ])
    username = StringField('Username пользователя',
                           validators=[
                               custom_length_check,
                               Regexp(regex=r'^[a-zA-Z0-9_]+$',
                                      message='Username пользователя может содержать только латинские буквы, цифры и нижнее подчеркивание')
                           ])
    nickname = StringField('Отображаемое имя',
                           validators=[
                               Length(min=1, max=30, message='Имя должно содержать от 1 до 30 символов')
                           ])
    description = StringField('О себе',
                              validators=[Length(max=150, message='Описание не должно быть длиннее 150 символов')])
    submit = SubmitField('Сохранить изменения')
