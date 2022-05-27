import logging
import sys

# Инициализация логера метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')  # Если не клиент, то сервер.
else:
    logger = logging.getLogger('client')  # Иначе это сервер.

class Port:
    def __set__(self, instance, value):
        if not 1023 < value <65536:
            logger.critical(f'Попытка запуска с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

# import ipaddress
# import logging
#
# logger = logging.getLogger('server')
#
#
# # Дескриптор для описания порта.
# class Port:
#     def __set__(self, instance, value):
#         if not 1023 < value < 65536:
#             logger.critical(f'Попытка запуска сервера с указанием неподходящего порта '
#                             f'{value}. Допустимый порт с 1024 до 65535')
#             exit(1)
#         instance.__dict__[self.name] = value  # Порт прошел проверку, добавляем его в список атрибутов экземпляра.
#
#     def __set_name__(self, owner, name):
#         self.name = name
#
#
# class Host:
#     def __set__(self, instance, value):
#         if value:
#             try:
#                 ip = ipaddress.ip_address(value)
#             except ValueError as e:
#                 logger.critical(f'Введен некорректный IP адрес{e}')
#                 exit(1)
#         instance.__dict__[self.name] = value
#
#     def __set_name__(self, owner, name):
#         self.name = name
