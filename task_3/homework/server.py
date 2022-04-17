import json
import socket
import sys
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTION, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


#  Принимаем сообщение клиента(словарь) и проверяем наличие всех данных в сообщениии и их корректность
def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])  # Парсим запрос проверяя его корректность
        else:
            listen_port = DEFAULT_PORT  # Или используем порт по умолчанию
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]  #  Загружаем адрес, который слушать
        else:
            listen_address = ''  # Или используем по умолчанию
    except IndexError:
        print('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Готовим сокет
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # подстраховка если порт занят
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTION)
#  Слушаем порт
    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)  # get_message from utils.py проверяет сообщение на корректность
            print(message_from_client)
            response = process_client_message(message_from_client) # проверяем данные на корректность
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()

if __name__ == '__main__':
    main()
