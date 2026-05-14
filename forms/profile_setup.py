from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class ProfileSetupForm(FlaskForm):
    avatar = FileField('Аватар',
                       validators=[
                           FileAllowed(['jpg', 'png', 'jpeg'], message='Недопустимый формат файла')
                       ])
    username = StringField('Имя пользователя',
                           validators=[
                               DataRequired(message='Поле должно быть заполнено'),
                               Length(min=4, max=20, message='Имя пользователя должно содержать от 5 до 20 символов'),
                               Regexp(regex=r'^[a-zA-Z0-9_]+$',
                                      message='Имя пользователя может содержать только латинские буквы, цифры и нижнее подчеркивание')
                           ])
    nickname = StringField('Отображаемое имя',
                           validators=[
                               DataRequired(message='Поле должно быть заполнено'),
                               Length(min=1, max=30, message='Имя должно содержать от 1 до 30 символов')
                           ])
    description = StringField('О себе',
                              validators=[Length(max=150, message='Описание не должно быть длиннее 150 символов')])
    submit = SubmitField('Создать аккаунт')
