"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
 Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
 В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
 («Узел доступен», «Узел недоступен»).
 При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""

from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(list_ip_addresses, timeout=1, requests=1):
    results = {'Available nodes': "", 'Not available nodes': ""}  # Получаем словарь с результатами
    for address in list_ip_addresses:
        try:
            address = ip_address(address)
        except ValueError:
            pass
        args = ["ping", "-c", str(requests), "-w", str(timeout), str(address)]  # Формируем запрос
        proc = Popen(args, shell=False, stdout=PIPE)
        proc.wait()  # ожидание выполнения команды
        # проверка кода завершения процесса 0- ОК-Узел доступен, 1-Узел не доступен
        if proc.returncode == 0:
            results['Available nodes'] += f"{str(address)}\n"
            res_string = f'{address} - Node available'
        else:
            results['Not available nodes'] += f"{str(address)}\n"
            res_string = f'{address} Node not available'
        print(res_string)
    return results


if __name__ == '__main__':
    ip_addresses = ['yandex.ru', '2.2.2.2', '192.168.0.100', '192.168.0.101', 'google.com']
    host_ping(ip_addresses)
