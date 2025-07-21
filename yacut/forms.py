from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import SHORT_LINK_REGEX, USER_SHORT_LINK_MAX_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, USER_SHORT_LINK_MAX_LENGTH),
                    Optional(),
                    Regexp(SHORT_LINK_REGEX)]
    )
    submit = SubmitField('Создать')
