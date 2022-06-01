"""Константы"""

import logging

DEFAULT_PORT = 7777  # Порт поумолчанию для сетевого ваимодействия
DEFAULT_IP_ADDRESS = '127.0.0.1'  # IP адрес по умолчанию для подключения клиента
MAX_CONNECTION = 5  # Максимальная очередь подключений
MAX_PACKAGE_LENGTH = 1024  # Максимальная длинна сообщения в байтах
ENCODING = 'utf-8'  # Кодировка проекта
LOGGING_LEVEL = logging.DEBUG  # Текущий уровень логирования
SERVER_CONFIG = 'server.ini'  # База данных для хранения данных сервера.

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'

# Словари-Ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}

