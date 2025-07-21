from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        parent_url = url_for('index_view', _external=True)
        return {
            'url': self.original,
            'short_link': f'{parent_url}{self.short}'
        }

    def from_dict(self, data):
        self.original = data['original']
        self.short = data['short']
