""" Decorators. """
import sys
import socket
import logging
import logs.config_client_log
import logs.config_server_log

sys.path.append('../')

# Метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


# Сам декоратор, выполняющий логирование вызовов функций. Сохраняет события типа debug, содержащие
# информацию о имени вызываемой функиции, параметры с которыми вызывается функция, и модуль, вызывающий функцию.


def log(func_to_log):
    def log_saver(*args, **kwargs):  # class-decorator
        logger.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs},'
                     f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)  # Обертка
        return ret
    return log_saver


# Декоратор, проверяющий, что клиент авторизован на сервере. Проверяет, что передаваемый объект сокета находится в
# списке авторизованных клиентов. За исключением передачи словаря-запроса на авторизацию.
# Если клиент не авторизован, генерирует исключение TypeError.
def login_required(func):
    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence сообщение. Если presense, то разрешаем.
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)
    return checker




