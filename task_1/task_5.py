"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import subprocess
import chardet

ARGS = ['ping', 'gb.ru']

YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
for line in YA_PING.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))

# yandex.ru
# 64 bytes from yandex.ru (5.255.255.55): icmp_seq=1 ttl=57 time=70.1 ms
# 64 bytes from yandex.ru (5.255.255.55): icmp_seq=2 ttl=57 time=70.3 ms
# 64 bytes from yandex.ru (5.255.255.55): icmp_seq=3 ttl=57 time=71.5 ms
# 64 bytes from yandex.ru (5.255.255.55): icmp_seq=4 ttl=57 time=70.5 ms
# google.ru
# 64 bytes from hem09s03-in-f3.1e100.net (216.58.209.195): icmp_seq=1 ttl=59 time=88.0 ms
# 64 bytes from bud02s22-in-f195.1e100.net (216.58.209.195): icmp_seq=2 ttl=59 time=89.8 ms
# 64 bytes from bud02s22-in-f3.1e100.net (216.58.209.195): icmp_seq=3 ttl=59 time=87.8 ms
# gb.ru
# 64 bytes from 178.248.232.209 (178.248.232.209): icmp_seq=1 ttl=58 time=68.1 ms
# 64 bytes from 178.248.232.209 (178.248.232.209): icmp_seq=2 ttl=58 time=70.5 ms
# 64 bytes from 178.248.232.209 (178.248.232.209): icmp_seq=3 ttl=58 time=68.8 ms
# 64 bytes from 178.248.232.209 (178.248.232.209): icmp_seq=4 ttl=58 time=94.4 ms
