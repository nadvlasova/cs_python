""" Launcher. Флаг  creationflags=subprocess.CREATE_NEW_CONSOLE нужен для ОС Windows,
чтобы каждый процесс запускался в отдельном окне консоли ."""
import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('gnome-terminal -- python3 server.py', shell=True))
        for i in range(2):  # что значит 2???
            PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -m send', shell=True))
        for i in range(5):  # что значит 5?
            PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -m listen', shell=True))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()


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