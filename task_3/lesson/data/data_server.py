""" Прогрмма сервера для получения приветствия от клиента и отправки ответа обратно."""

from socket import socket, AF_INET, SOCK_STREAM

SERV_SOCK = socket(AF_INET, SOCK_STREAM)  # Создаем сокет TCP.
SERV_SOCK.bind(('', 8888))  # Связываем сокет с адресом и портом через который клиент подключится к серверу.
SERV_SOCK.listen(3)  # Сокет слушает-ждет запросы, одновременно сможет принять 3.

try:
    while True:
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()  # Принимает запрос на подключение клиентов.
        DATA = CLIENT_SOCK.recv(1024) # Указываем размер максимального кол-ва байт сообщения.
        print(f"Сообщение: {DATA.decode('utf-8') } было отправлено клиентом: {ADDR}")
        MSG = 'Привет клиент!'
        CLIENT_SOCK.send(MSG.encode('utf-8'))
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()