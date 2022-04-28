import argparse
import json
import logging
import socket
import sys
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTION, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError
import logs.config_server_log
from decos import log

#  Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


#  Принимаем сообщение клиента(словарь) и проверяем наличие всех данных в сообщениии и их корректность
@log
def process_client_message(message):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


# Парсер аргументов командной строки.
@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')  # ??????
    parser.add_argument('-a', default='', nargs='?')  # ?????
    return parser


# Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию.
def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # Проверка получения корректного порта для работы сервера.
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port},'
                       f'адрес с которого принимаются подключения: {listen_address}.'
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Подготовка сокета.
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Готовим сокет
    transport.bind((listen_address, listen_port))

    #  Слушаем порт
    transport.listen(MAX_CONNECTION)
    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}.')
        try:
            message_from_client = get_message(client)  # get_message from utils.py проверяет сообщение на корректность
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}.')
            response = process_client_message(message_from_client)  # проверяем данные на корректность
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}.')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
