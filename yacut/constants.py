"""Константы приложения yacut."""
import re

from string import digits, ascii_lowercase, ascii_uppercase


USER_SHORT_LINK_MAX_LENGTH = 16
"""Максимально допустимая длина пользовательской короткой ссылки."""

RANDOM_SHORT_LINK_MAX_LENGTH = 6
"""Максимально допустимая длина сгенерированной короткой ссылки."""

ACCEPTED_SHORT_LINK_CHARS = f'{ascii_uppercase}{ascii_lowercase}{digits}'
"""Строка допустимых символов для коротких ссылок."""

SHORT_LINK_REGEX = re.compile(f'^[{re.escape(ACCEPTED_SHORT_LINK_CHARS)}]+$')
"""Регулярное выражение дла валидации коротких ссылок."""
