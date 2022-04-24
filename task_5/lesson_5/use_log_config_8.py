""" Вынесение настройки логгирования в отдельный модуль - log_config_7
т.е. здесь мы импортируем файл с кодом логирования и запускаем его из этого файла. """

import logging

LOG = logging.getLogger('app_7.log')

def main():
    """ Тестовая главная функция!"""
    LOG.debug('Старт приложения!')

if __name__ == '__main__':
    main()
