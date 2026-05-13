from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Length


class AddPost(FlaskForm):
    text = StringField('Что нового?',
                       validators=[
                           Length(max=1000, message='Текст поста не может превышать 1000 символов')
                       ])
    image = FileField('Выбрать фото',
                      validators=[
                          FileAllowed(['jpg', 'png', 'jpeg'], message='Недопустимый формат файла')
                      ])
    submit = SubmitField('Опубликовать')
