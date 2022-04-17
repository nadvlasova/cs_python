
import subprocess
import time

process = []

while True:
    action = input('Выберите действие: q - выход , s - запустить сервер и клиенты, t - запустить только клиентов , x - закрыть все окна:')

    if action == 'q':
        break
    elif action == 's':

        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        #start server
        process.append(subprocess.Popen('gnome-terminal -- python3 time_server.py', shell=True))

        # Запускаем клиентов:
        time.sleep(0.5)
        for i in range(clients_count):
            process.append(subprocess.Popen(f'gnome-terminal -- python3 time_client.py -n Test{i}', shell=True))
    elif action == 't':

        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))

        # Запускаем клиентов:
        time.sleep(0.5)
        for i in range(clients_count):
            process.append(subprocess.Popen(f'gnome-terminal -- python3 time_client.py -n Test{i}', shell=True))

    elif action == 'x':
        while process:
            victim = process.pop()
            victim.kill()
            victim.terminate()