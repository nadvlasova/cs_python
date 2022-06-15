"""
Класс - исключение, для обработки ошибок сервера.
При генерации требует строку с описанием ошибки,
полученную с сервера.
"""


class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
