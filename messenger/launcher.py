""" Launcher. Флаг  creationflags=subprocess.CREATE_NEW_CONSOLE нужен для ОС Windows,
чтобы каждый процесс запускался в отдельном окне консоли ."""
import random
import subprocess
import time

PROCESSES = []


def get_name(i):
    return f'{random.getrandbits(128)}/{i}'


while True:
    ACTION = input('Выберите действие: q - выход,'
                   'sc - запустить сервер и клиентов,'
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 'sc':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        # Стартуем сервер!!!
        PROCESSES.append(subprocess.Popen('gnome-terminal -- python3 server.py', shell=True))
        # Стартуем клиентов!!!
        time.sleep(0.5)
        for i in range(clients_count):
            PROCESSES.append(subprocess.Popen(f'gnome-terminal -- python3 client.py -n Test{i}', shell=True))
    elif ACTION == 'x':
        while PROCESSES:
            PROCESSES.pop().kill()
