import ipaddress
import logging

logger = logging.getLogger('server')


# Дескриптор для описания порта.
class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                            f'{value}. Допустимый порт с 1024 до 65535')
            exit(1)
        instance.__dict__[self.name] = value  # Порт прошел проверку, добавляем его в список атрибутов экземпляра.

    def __set_name__(self, owner, name):
        self.name = name


class Host:
    def __set__(self, instance, value):
        if value:
            try:
                ip = ipaddress.ip_address(value)
            except ValueError as e:
                logger.critical(f'Введен некорректный IP адрес{e}')
                exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
