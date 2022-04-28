import argparse
import sys
import json
import socket
import time
import logging
import logs.config_client_log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
from errors import ReqFieldMissingError
from decos import log


# Инициализация клиентского логгера.
CLIENT_LOGGER = logging.getLogger('client')


# Функция генерации запроса о присутствии клиента на сервере
@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


# Функция разбирает ответ сервера и возвращает статус
@log
def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


#  Создание парсера аргументов командной строки.
@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')  # ?????
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


#  Загрузка параметров командной строки.
def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr  # Определение адреса
    server_port = namespace.port  # Определение порта

    # проверка подхлдящего номаера порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: '
                       f'адрес сервера: {server_address}, порт: {server_port}.')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))  # Подключаемся к серверу
        message_to_server = create_presence()  # create_presence- Генерируем запрос о присутствии
        send_message(transport, message_to_server)  # Подготавливаем и отправляем сообщение
        answer = process_ans(get_message(transport))  # Ответ с сервера, process_ans-проверяем его доступность
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port},'
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
