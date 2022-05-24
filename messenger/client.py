import argparse
import sys
import json
import socket
import threading
import time
import logging
import logs.config_client_log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, SENDER, MESSAGE_TEXT, EXIT, DESTINATION
from common.utils import get_message, send_message
from errors import ReqFieldMissingError, ServerError, IncorrectDataRecivedError
from decos import log
from messenger.metaclasses import ClientVerifier

# Инициализация клиентского логгера.
logger = logging.getLogger('client')


# Класс формировки и отправки сообщений на сервер и взаимодействия с пользователем.
class ClientSender(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    # Функция создает словарь с сообщением о выходе."""
    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    # Функция запрашивает кому отправить сообщение и текст сообщениия и отправляет полученные данные на сервер."""
    def create_message(self):
        to = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(self.sock, message_dict)
            logger.info(f'Отправлено сообщение для пользователя {to}')
        except:
            logger.critical('Потеряно соединение с сервером.')
            exit(1)

    # Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения.
    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                try:
                    send_message(self.sock, self.create_exit_message())
                except:
                    pass
                print('Завершение соединения!')
                logger.info('Завершение работы по команде пользователя.')
                time.sleep(5)  # Задержка необходима, чтобы успело уйти сообщение о выходе
                break
            else:
                print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды.')

    # Функция выводящая справку по используемым командам.
    def print_help(self):
        print('Поддерживаемые команды: ')
        print('message - отправить сообщение. Кому и текст будет запрошено отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')


# Класс-приемник сообщений с сервера. Принимает сообщения, выводит в консоль.
class ClientReader(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    # Функция обработчик сообщений других пользователей поступающих с сервера. """
    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and \
                        SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                    logger.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                else:
                    logger.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                logger.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                logger.critical(f'Потеряно соединение с сервером.')
                time.sleep(20)
                print(logger.critical())
                break


# Функция генерации запроса о присутствии клиента на сервере
@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


# Функция разбирает ответ сервера и возвращает статус
@log
def process_ans(message):
    logger.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


"""Создание парсера аргументов командной строки. Читаем параметры, возвращаем 3 параметра.
nargs='?' - если присутствует один аргумент – он будет сохранён, иначе – будет использовано значение 
из ключа defaullogger"""


@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    # проверка подходящего номера порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name


def main():
    # Сообщаем о запуске.
    print('Консольный менеджер. Клиентский модуль.')

    #  Загрузка параметров командной строки.
    server_address, server_port, client_name = create_arg_parser()

    # Если имя пользователя не было передано, необходимо запросить пользователя.
    if not client_name:
        client_name = input('Введите имя пользователя: ')
    else:
        print(f'Клиентский модуль запущен с именем: {client_name}')

    logger.info(f'Запущен клиент с параметрами: '
                f'адрес сервера: {server_address}, порт: {server_port}, имя пользователя: {client_name}.')

    # Инициализация сокета и сообщение серверу о нашем появлении.
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))  # Подключаемся к серверу
        send_message(transport, create_presence(client_name))  # Подготавливаем и отправляем сообщение
        answer = process_ans(get_message(transport))  # Ответ с сервера, process_ans-проверяем его доступность
        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')
        exit(1)
    except ServerError as error:
        logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        exit(1)
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(f'Не удалось подключиться к серверу {server_address}:{server_port},'
                        f'конечный компьютер отверг запрос на подключение.')
        exit(1)
    # Если соединение с сервером корректно, запускаем клиентский процесс приёма сообщений.
    else:
        module_receiver = ClientReader(client_name, transport)
        module_receiver.daemon = True
        module_receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        module_sender = ClientSender(transport, client_name)
        module_sender.daemon = True
        module_sender.start()
        logger.debug('Запущены процессы.')

        # Watchdog основной цикл, если один из потоков завершён, то значит или потеряно соединение,
        # или пользователь ввел exit. Поскольку все события обрабатываются в потоках, достаточно просто завершить цикл."""
        while True:
            time.sleep(1)
            if module_receiver.is_alive() and module_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
