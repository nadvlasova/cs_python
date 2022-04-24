import json

from messenger.common.variables import MAX_PACKAGE_LENGTH, ENCODING

"""Утилита приема и декодирования сообщения, принимает байты и выдает словарь, 
если вместо или вместе с байтами приходит чтщ-то другое - выдает ошибку"""


def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


"""Утилита кодирования и отправки сообщения, принимает словарь и отправляет его"""


def send_message(sock, message):
    js_message = json.dumps(message)  # Дампим(сбрасывать) сообщение
    encoded_message = js_message.encode(ENCODING)  # Энкодим это сообщение
    sock.send(encoded_message)
