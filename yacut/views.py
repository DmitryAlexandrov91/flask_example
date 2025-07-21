from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import create_flash_render, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original = form.original_link.data
    short = form.custom_id.data
    existing_url = URLMap.query.filter_by(original=original).first()
    if short is not None:
        url = URLMap.query.filter_by(short=short).first()
        if url is not None:
            flash(
                'Предложенный вариант короткой ссылки уже существует.',
                'info'
            )
            return render_template('index.html', form=form)
        url = URLMap(
            original=original,
            short=short
        )
        return create_flash_render(form, url)
    if existing_url is not None:
        existing_url.short = get_unique_short_id()
        return create_flash_render(db, form, existing_url, add=False)
    random_short_id = get_unique_short_id()
    url = URLMap(
        original=form.original_link.data,
        short=random_short_id
    )
    return create_flash_render(form, url)


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(f'{url.original}')
