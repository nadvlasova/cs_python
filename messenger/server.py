import argparse
import json
import logging
import select
import socket
import sys
import time

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTION, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, RESPONSE_200, RESPONSE_400, DESTINATION, \
    EXIT
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError
import logs.config_server_log
from decos import log

#  Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')

"""Принимаем сообщение клиента(словарь) и проверяем наличие всех данных в сообщениии и их корректность.
Отправляем ответ(словарь) для клиента с результатом приема."""


@log
def process_client_message(message, messages_list, client, clients, names):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}.')
    #  Если это сообщение о присутствии, принимаем и отвечаем.
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        # Если такой пользователь ещё не зарегистрирован, регистрируем, иначе отправляем ответ и завершаем соединение.
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    # Если это это сообщение, то добавляем в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and \
            TIME in message and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    #  Если клиент выходит:
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    # Иначе отдаем Bad Request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client, response)
        return

"""Функция адресной отправки сообщения определенному клиенту. Принимает словарь сообщение, 
список зарегистрированных пользователей и слушающие сокеты. Ничего не возвращает."""
@log
def process_message(message, names, listen_socks):
    # message[DESTINATION] - имя
    # names[message[DESTINATION]] - получатель
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(f'Пользователь {message[DESTINATION]}не зарегистрирован на сервере,'
                            f' отправка сообщений невозможна!')

# Парсер аргументов командной строки.
@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # Проверка получения корректного порта для работы сервера.
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    return listen_address, listen_port


# Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию.
def main():
    # global OSError
    listen_address, listen_port = create_arg_parser()

    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port},'
                       f'адрес с которого принимаются подключения: {listen_address}.'
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Подготовка сокета.
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Готовим сокет
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # Список клиентов, очередь сообщений.
    clients = []
    messages = []

    # Словарь содержащий имена пользователей и соответствующие им сокеты.
    names = dict()

    #  Слушаем порт
    transport.listen(MAX_CONNECTION)
    # Основной цикл программы сервера.
    while True:
        # Ждем подключений, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}.')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        # Проверяем на наличие ждущих клиентов.
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass
        # Принимаем сообщения и если они есть, кладем их в словарь, если ошибка, то исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message, clients, names)
                except Exception:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения обрабатываем каждое.
        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
