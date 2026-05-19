from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Length, ValidationError


class FileSizeLimit:
    def __init__(self, max_size_mb):
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def __call__(self, form, field):
        if field.data:
            field.data.seek(0, 2)
            size = field.data.tell()
            field.data.seek(0)

            if size > self.max_size_bytes:
                raise ValidationError(f'Размер файла не должен превышать {self.max_size_mb} МБ')


class AddPost(FlaskForm):
    text = StringField('Что нового?',
                       validators=[
                           Length(max=1000, message='Текст поста не может превышать 1000 символов')
                       ])
    image = FileField('Выбрать фото',
                      validators=[
                          FileAllowed(['jpg', 'png', 'jpeg'], message='Недопустимый формат файла'),
                          FileSizeLimit(max_size_mb=20)
                      ])
    submit = SubmitField('Опубликовать')
