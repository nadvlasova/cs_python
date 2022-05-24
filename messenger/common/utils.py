import json
import sys
from messenger.common.variables import MAX_PACKAGE_LENGTH, ENCODING
from messenger.decos import log
from messenger.errors import IncorrectDataRecivedError, NonDictInputError
sys.path.append('../')

"""Утилита приема и декодирования сообщения, принимает байты и выдает словарь, 
если вместо или вместе с байтами приходит что-то другое - выдает ошибку"""

@log
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)  # получаем строку в байтах
    if isinstance(encoded_response, bytes):  # Проверка входных данных
        json_response = encoded_response.decode(ENCODING) # Декодируем в UTF-8
        response = json.loads(json_response)  # Переводим данные в словарь
        if isinstance(response, dict):
            return response
        raise IncorrectDataRecivedError
    raise IncorrectDataRecivedError


"""Утилита кодирования и отправки сообщения, принимает словарь и отправляет его"""

@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise NonDictInputError
    js_message = json.dumps(message)  # Дампим(сбрасывать) сообщение
    encoded_message = js_message.encode(ENCODING)  # Энкодим это сообщение
    sock.send(encoded_message)
