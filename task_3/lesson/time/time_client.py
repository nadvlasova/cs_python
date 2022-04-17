""" Программа клиента времени. """

from socket import socket, AF_INET, SOCK_STREAM

try:
    while True:
            # создаем объект клиентского сокета
            CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
            # соединяемся с сервером
            CLIENT_SOCK.connect(('localhost', 8888))
            # 1024 это размер пакета, если пришло не 1024, но уже что-то пришло, он вернёт всё, что имеется.
            TIME_BYTES = CLIENT_SOCK.recv(1024)
            CLIENT_SOCK.close()
            print(f"Текущее время {TIME_BYTES.decode('utf-8')}")
finally:
    CLIENT_SOCK.close()
