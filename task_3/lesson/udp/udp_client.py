"""Программа клиента, передающего серверу сообщение при каждом запросе на соединение."""

from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST

CLIENT_SOCK = socket(AF_INET, SOCK_DGRAM)  # Определяем UDP-протокол
CLIENT_SOCK.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # Включаем опцию (1) ???  Определяем широковещательные пакеты

try:
    MSG = 'Привет сервер!'
    CLIENT_SOCK.sendto(MSG.encode('utf-8'), ('localhost', 8888))
    MSG, ADDR = CLIENT_SOCK.recvfrom(1024)
    print(MSG.decode('utf-8'))
finally:
    CLIENT_SOCK.close()