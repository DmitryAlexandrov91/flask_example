from http import HTTPStatus

from flask import jsonify, request
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import (data_update_and_create_object, get_unique_short_id,
                    validate_short_id)


@app.route('/api/id/', methods=['POST'])
def add_short():
    try:
        data = request.get_json()
    except (BadRequest, UnsupportedMediaType):
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    original = data['url']
    data['original'] = original
    short_id = data.get('custom_id')
    if short_id:
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.')
        if not validate_short_id(short_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        return data_update_and_create_object(data, short_id)
    existing_url = URLMap.query.filter_by(original=original).first()
    random_short_id = get_unique_short_id()
    if existing_url is not None:
        existing_url.short = random_short_id
        db.session.commit()
        return jsonify(existing_url.to_dict()), HTTPStatus.CREATED
    return data_update_and_create_object(data, random_short_id)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
