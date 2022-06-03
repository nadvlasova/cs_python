""" Decorators. """
import sys
import logging
import logs.config_client_log
import logs.config_server_log

""" Метод определения модуля, источника запуска. Метод find() возвращает индекс
первого вхождения искомой подстроки, если он найден, в противном случае возвращает -1. """

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')

""" Сам декоратор."""


def log(func_to_log):
    def log_saver(*args, **kwargs):  # class-decorator
        logger.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs},'
                     f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)  # Обертка
        return ret
    return log_saver


