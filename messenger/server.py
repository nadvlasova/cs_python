import argparse
import json
import logging
import select
import socket
import sys
import threading
import time
from common.variables import *
from common.utils import *
from errors import IncorrectDataRecivedError
import logs.config_server_log
from decos import log
from descripts import Port
from metaclasses import ServerVerifier

#  Инициализация логирования сервера.
from server_database import ServerStorage

logger = logging.getLogger('server')


# Парсер аргументов командной строки.
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


# Основной класс сервера.
class Server(threading.Thread, metaclass=ServerVerifier):
    port = Port()

    # addr = Host()

    def __init__(self, listen_address, listen_port, database):
        # Параметры подключения.
        self.addr = listen_address
        self.port = listen_port

        self.database = database  # База данных сервера.

        self.clients = []  # Список подключенных клиентов.

        self.messages = []  # Список сообщений на отправку.

        self.names = dict()  # Словарь содержащий сопоставленные имена и соответствующие им сокеты.

        super().__init__()  # Конструктор предка.

    def init_socket(self):
        logger.info(f'Запущен сервер, порт для подключений: {self.port},'
                    f'адрес с которого принимаются подключения: {self.addr}.'
                    f'Если адрес не указан, принимаются соединения с любых адресов.')

        # Подготовка сокета.
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        #  Слушаем сокет
        self.sock = transport
        self.sock.listen()

    def run(self):
        self.init_socket()

        # Основной цикл программы сервера.
        while True:
            # Ждем подключений, если таймаут вышел, ловим исключение.
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соединение с ПК {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            # Проверяем на наличие ждущих клиентов.
            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            # Принимаем сообщения и если они есть, кладем их в словарь, если ошибка, то исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except:
                        logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                        self.clients.remove(client_with_message)

            # Если есть сообщения обрабатываем каждое.
            for message in self.messages:
                try:
                    self.process_message(message, send_data_lst)
                except:
                    logger.info(f'Связь с клиентом с именем {message[DESTINATION]} была потеряна')
                    self.clients.remove(self.names[message[DESTINATION]])
                    del self.names[message[DESTINATION]]
            self.messages.clear()

    # Функция адресной отправки сообщения определенному клиенту. Принимает словарь сообщение,
    # список зарегистрированных пользователей и слушающие сокеты. Ничего не возвращает."""

    def process_message(self, message, listen_socks):
        # message[DESTINATION] - имя
        # names[message[DESTINATION]] - получатель
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            logger.error(f'Пользователь {message[DESTINATION]}не зарегистрирован на сервере,'
                         f' отправка сообщений невозможна!')

    # Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента, проверяет корректность, отправляет
    # словарь-ответ в случае необходимости.
    def process_client_message(self, message, client):
        logger.debug(f'Разбор сообщения от клиента : {message}')
        #  Если это сообщение о присутствии, принимаем и отвечаем.
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            # Если такой пользователь ещё не зарегистрирован, регистрируем, иначе отправляем ответ и завершаем соединение.
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        # Если это это сообщение, то добавляем в очередь сообщений. Ответ не требуется.
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and \
                TIME in message and SENDER in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            return
        #  Если клиент выходит:
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.database.user_logout(message[ACCOUNT_NAME])
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[ACCOUNT_NAME]
            return
        # Иначе отдаем Bad Request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            send_message(client, response)
            return


def print_help():
    print('Поддеоживаемые команды: ')
    print('users - список известных пользователей.')
    print('connected - список подключенных пользователей.')
    print('loghist - история входов пользователя.')
    print('exit - завершение работы сервера.')
    print('help - вывод справки по поддерживаемым командам.')


def main():
    # Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    listen_address, listen_port = arg_parser()

    # Инициализация базы данных
    database = ServerStorage()

    # Создание экземпляра класса - сервера и его запуск.
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Выводим справку.
    print_help()

    # Основной цикл сервера.
    while True:
        command = input('Введите команду: ')
        if command == 'help':
            print_help()
        elif command == 'exit':
            break
        elif command == 'users':
            for user in sorted(database.users_list()):
                print(f'Пользователь {user[0]}, последний вход: {user[1]}')
        elif command == 'connected':
            for user in sorted(database.active_users_list()):
                print(f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, время установки соединения: {user[3]}')
        elif command == 'loghist':
            name = input('Введите имя пользователя для просмотра его истории. '
                         'Для вывода всей истории, просто нажмите Enter: ')
            for user in sorted(database.login_history(name)):
                print(f'Пользователь: {user[0]} время входа: {user[1]}. Вход с: {user[2]}:{user[3]}')
        else:
            print('Команда не распознана. Введите команду из предложенных в списке.')


if __name__ == '__main__':
    main()
