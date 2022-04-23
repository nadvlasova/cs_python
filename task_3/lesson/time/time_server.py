""" Программф сервера времени."""

import socket
import time

# создаем объект серверного сокета
# сетевой протокол (TCP)
SERV_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# связываем сокет с адресом и портом
# именно через них клиент подключится к серверу ''-это IP клиента
SERV_SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # это спец. функция переиспользовать порт если он занят
SERV_SOCK.bind(('', 8888))


# listen - сокет готов к прослушиванию
# Метод принимает один аргумент-максимальное количество подключений в очереди.
SERV_SOCK.listen(6)

try:
    while True:
        # принимает запрос на установку подключения клиентов
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()  #  когда сервер занят, никто другой не может к нему отбратиться
        print(f'Получен запрос на соединение от клиента с адресом и портом: {ADDR}')
        TIMESTR = time.ctime(time.time()) + "\n"
        # отправляем клиенту сообщение
        CLIENT_SOCK.send(TIMESTR.encode('utf-8'))
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()
