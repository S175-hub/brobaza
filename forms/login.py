from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Email',
                       validators=[
                           DataRequired(message='Поле должно быть заполнено'),
                           Email(message='Введите корректный email')
                       ])
    password = PasswordField('Пароль',
                             validators=[
                                 DataRequired(message='Поле должно быть заполнено')
                             ])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
