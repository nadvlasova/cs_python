import logging
import sys

# Инициализация логера метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')  # Если не клиент, то сервер.
else:
    logger = logging.getLogger('client')  # Иначе это клиент.


# Класс - дескриптор для номера порта. Позволяет использовать только порты с 1023 по 65536.
# При попытке установить неподходящий номер порта генерирует исключение.

class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
