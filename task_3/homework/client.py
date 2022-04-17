import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message


# Функция генерации запроса о присутствии клиента на сервере
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


# Функция разбирает ответ сервера и возвращает статус
def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_address = sys.argv[2]  # Определение адреса
        server_port = int(sys.argv[3])  # Определение порта
        if server_port < 1024 or server_port > 65535:  # Проверка валидности порта
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))  # Подключаемся к серверу
    message_to_server = create_presence()  # create_presence- Генерируем запрос о присутствии
    send_message(transport, message_to_server)  # Подготавливаем и отправляем сообщение
    try:
        answer = process_ans(get_message(transport))  # Ответ с сервера, process_ans-проверяем его доступность
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера!')


if __name__ == '__main__':
    main()
