"""Утилитки приложения yacut."""
from http import HTTPStatus
from random import choice

from flask import flash, jsonify, render_template

from yacut import db

from .constants import (ACCEPTED_SHORT_LINK_CHARS,
                        RANDOM_SHORT_LINK_MAX_LENGTH, SHORT_LINK_REGEX,
                        USER_SHORT_LINK_MAX_LENGTH)
from .models import URLMap


def generate_short_id() -> str:
    """Генерит случайную строку из допустимых символов."""
    random_short_string = ''.join(
        choice(ACCEPTED_SHORT_LINK_CHARS) for _ in range(
            RANDOM_SHORT_LINK_MAX_LENGTH)
    )
    return random_short_string


def get_unique_short_id() -> str:
    """Возвращает уникальную сгенирированную короткую ссылку."""
    random_short_id = generate_short_id()
    while URLMap.query.filter_by(short=random_short_id).first():
        random_short_id = generate_short_id()
    return random_short_id


def create_flash_render(form, obj, add=True, db=db):
    """DRY функция для index_view.

    Опционально добавляет объект в бд,
    создаёт flash сообщение и возвращает страницу.

    """
    if add:
        db.session.add(obj)
    db.session.commit()
    flash(f'{obj.short}', 'url_gen')
    return render_template('index.html', form=form)


def validate_short_id(short_id: str) -> bool:
    """Проверяет short_id на длину и допустимые символы."""
    return (len(short_id) <= USER_SHORT_LINK_MAX_LENGTH and
            SHORT_LINK_REGEX.match(short_id) is not None
            )


def data_update_and_create_object(data, new_value, db=db):
    """DRY функция для add_short.

    Обновляет data, создаёт объект в бд и возвращает ответ
    в виде json словаря.

    """
    data['short'] = new_value
    obj = URLMap()
    obj.from_dict(data)
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.to_dict()), HTTPStatus.CREATED
