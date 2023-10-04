class HTTPStatusError(Exception):
    """Отсутствие ожидаемого статуса."""


class MissedStatusError(Exception):
    """Отсутствие статуса работы."""
