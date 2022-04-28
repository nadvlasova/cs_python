""" Decorators. """
import inspect
import sys
import logging
import traceback

import logs.config_client_log
import logs.config_server_log

""" Метод определения модуля, источника запуска. Метод find() возвращает индекс
первого вхождения искомой подстроки, если он найден, в противном случае возвращает -1. """

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')

""" Сам декоратор."""


def log(func_to_log):
    def log_saver(*args, **kwargs):  # class-decorator
        ret = func_to_log(*args, **kwargs)  # Обертка
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs},'
                     f'Вызов из модуля {func_to_log.__module__}')
        return ret

    return log_saver


# """ Реализация в виде класса @log() """
#
#
# class Log:
#     def __call__(self, func_to_log):  # class-decorator
#         def log_saver(*args, **kwargs):
#             ret = func_to_log(*args, **kwargs)  # Обертка
#             LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} с параметрами {args}, {kwargs},'
#                          f'Вызов из модуля {func_to_log.__module__}'
#                          f'Вызов из функции {traceback.extract_stack()[0].strip().split()[-1]}.'
#                          f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
#             return ret
#
#         return log_saver
