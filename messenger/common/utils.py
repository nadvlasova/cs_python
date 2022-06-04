import json
import sys
from common.variables import *
from common.decos import log
sys.path.append('../')

# Утилита приема и декодирования сообщения, принимает байты и выдает словарь,
# если вместо или вместе с байтами приходит что-то другое - выдает ошибку"""

@log
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)  # получаем строку в байтах
    json_response = encoded_response.decode(ENCODING)  # Декодируем в UTF-8
    response = json.loads(json_response)  # Переводим данные в словарь
    if isinstance(response, dict):
        return response
    else:
        raise TypeError

# Утилита кодирования и отправки сообщения, принимает словарь и отправляет его

@log
def send_message(sock, message):
    js_message = json.dumps(message)  # Дампим(сбрасывать) сообщение
    encoded_message = js_message.encode(ENCODING)  # Энкодим это сообщение
    sock.send(encoded_message)
