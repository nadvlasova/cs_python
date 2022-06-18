""" Launcher. Флаг  creationflags=subprocess.CREATE_NEW_CONSOLE нужен для ОС Windows,
чтобы каждый процесс запускался в отдельном окне консоли ."""
import random
import subprocess
import time


def main():
    process = []

    while True:
        action = input(
            'Выберите действие: q - выход , s - запустить сервер, '
            'k - запустить клиенты x - закрыть все окна:')
        if action == 'q':
            break
        elif action == 's':
            # Запускаем сервер!
            process.append(
                subprocess.Popen('gnome-terminal -- python3 server.py',
                                 stdout=subprocess.PIPE, stderr=None, shell=True))
        elif action == 'k':
            print('Убедитесь, что на сервере зарегистрировано необходимое '
                  'количество клиентов с паролем 1.')
            print('Первый запуск может быть достаточно долгим '
                  'из-за генерации ключей!')
            clients_count = int(
                input('Введите количество тестовых клиентов для запуска: '))
            # Запускаем клиентов:
            for i in range(clients_count):
                process.append(
                    subprocess.Popen(
                        f'gnome-terminal -- python3 client.py -n test{i} -p {i}',
                        shell=True))
        elif action == 'x':
            while process:
                process.pop().kill()


if __name__ == '__main__':
    main()








# def main():
#     process = []
#
#     while True:
#         action = input(
#             'Выберите действие: q - выход , s - запустить сервер, '
#             'k - запустить клиенты x - закрыть все окна:')
#         if action == 'q':
#             break
#         elif action == 's':
#             # Запускаем сервер!
#             process.append(
#                 subprocess.Popen('gnome-terminal -- python server.py',
#                                  shell=True))
#         elif action == 'k':
#             print('Убедитесь, что на сервере зарегистрировано необходимое '
#                   'количество клиентов с паролем 1.')
#             print('Первый запуск может быть достаточно долгим '
#                   'из-за генерации ключей!')
#             clients_count = int(
#                 input('Введите количество тестовых клиентов для запуска: '))
#             # Запускаем клиентов:
#             for i in range(clients_count):
#                 process.append(
#                     subprocess.Popen(
#                         f'gnome-terminal -- python client.py -n Test{i + 1} -p 1',
#                         shell=True))
#         elif action == 'x':
#             while process:
#                 process.pop().kill()
#
#
# if __name__ == '__main__':
#     main()

# PROCESSES = []
#
#
# def get_name(i):
#     """ Консольный вариант запуска мессенджера."""
#     return f'{random.getrandbits(128)}/{i}'
#
#
# while True:
#     ACTION = input('Выберите действие: q - выход,'
#                    'sc - запустить сервер и клиентов,'
#                    'x - закрыть все окна: ')
#
#     if ACTION == 'q':
#         break
#     elif ACTION == 'sc':
#         clients_count = int(input('Введите количество тестовых клиентов '
#                                   'для запуска: '))
#         # Стартуем сервер!!!
#         PROCESSES.append(subprocess.Popen(
#             'gnome-terminal -- python3 server.py', shell=True))
#         # Стартуем клиентов!!!
#         time.sleep(0.5)
#         for i in range(clients_count):
#             PROCESSES.append(subprocess.Popen(
#                 f'gnome-terminal -- python3 client.py -n Test{i}', shell=True))
#     elif ACTION == 'x':
#         while PROCESSES:
#             PROCESSES.pop().kill()
