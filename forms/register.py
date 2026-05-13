from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class RegisterForm(FlaskForm):
    email = EmailField('Email',
                       validators=[
                           DataRequired(message='Поле должно быть заполнено'),
                           Email(message='Введите корректный email')
                       ])
    password = PasswordField('Пароль',
                             validators=[
                                 DataRequired(message='Поле должно быть заполнено'),
                                 Length(min=8, message='Минимальная длина пароля — 8 символов')
                             ])
    confirm_password = PasswordField('Повторите пароль',
                                     validators=[
                                         DataRequired(message='Поле должно быть заполнено'),
                                         EqualTo('password', message='Пароли не совпадают')
                                     ])
    submit = SubmitField('Далее')
