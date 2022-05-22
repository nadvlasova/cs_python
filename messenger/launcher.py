""" Launcher. Флаг  creationflags=subprocess.CREATE_NEW_CONSOLE нужен для ОС Windows,
чтобы каждый процесс запускался в отдельном окне консоли ."""
import random
import subprocess
import time


PROCESSES = []

while True:
    ACTION = input('Выберите действие: q - выход,'
                   'sc - запустить сервер и клиентов,'
                   'c - запустить только клиентов,'
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
    elif ACTION == 'c':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        time.sleep(0.5)
        for i in range(clients_count):
            PROCESSES.append(subprocess.Popen(f'gnome-terminal -- python3 client.py -n Test{i}', shell=True))
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
            VICTIM.terminate()




# PROCESSES = []
#
#
# def get_name(i):
#     return f'{random.getrandbits(128)}/{i}'
#
#
# while True:
#     ACTION = input('Выберите действие: q - выход,'
#                    's - запустить сервер и клиенты,'
#                    'x - закрыть все окна: ')
#
#     if ACTION == 'q':
#         break
#     elif ACTION == 's':
#         # clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
#         PROCESSES.append(subprocess.Popen('gnome-terminal -- python3 server.py', shell=True))
#
#         time.sleep(0.5)
#         for i in range(2):
#             # Добавляем на случай если имена 1-2-3 бывают заняты
#             name = get_name(i)
#             PROCESSES.append(subprocess.Popen(f'gnome-terminal -- python3 client.py -n Test{i}', shell=True))
#     elif ACTION == 'x':
#         while PROCESSES:
#             VICTIM = PROCESSES.pop()
#             VICTIM.kill()



# # Лаунчер для task_7
# PROCESS = []
#
# while True:
#     ACTION = input('Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна: ')
#
#     if ACTION == 'q':
#         break
#     elif ACTION == 's':
#         PROCESS.append(subprocess.Popen('gnome-terminal -- python3 server.py', shell=True))
#         for i in range(2):
#             PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -m send', shell=True))
#         for i in range(5):
#             PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -m listen', shell=True))
#     elif ACTION == 'x':
#         while PROCESS:
#             VICTIM = PROCESS.pop()
#             VICTIM.kill()


# PROCESS = []
#
# while True:
#     ACTION = input('Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна: ')
#
#     if ACTION == 'q':
#         break
#     elif ACTION == 's':
#         PROCESS.append(subprocess.Popen('python server.py',
#                                         creationflags=subprocess.CREATE_NEW_CONSOLE))
#         for i in range(2):  # что значит 2???
#             PROCESS.append(subprocess.Popen('python client.py -m send',
#                                             creationflags=subprocess.CREATE_NEW_CONSOLE))
#             for i in range(5):  # что значит 5?
#                 PROCESS.append(subprocess.Popen('python client.py -m listen',
#                                                 creationflags=subprocess.CREATE_NEW_CONSOLE))
#     elif ACTION == 'x':
#         while PROCESS:
#             VICTIM = PROCESS.pop()
#             VICTIM.kill()
