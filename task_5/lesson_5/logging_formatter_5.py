""" Обработчики. Передача своих переменных в логгер."""

import logging

LOG = logging.getLogger('app')

FILE_HANDLER = logging.FileHandler("app_5.log", encoding='utf-8')

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s -%(message)s")

FILE_HANDLER.setFormatter(FORMATTER)

PARAMS = {'host': 'www.python.org', 'port': 80}

LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

LOG.info('Параметры подключения: %(host)s, %(port)d', PARAMS)
LOG.info(f"Параметры подключения: {PARAMS['host']}")
LOG.warning('Warning!')
LOG.critical('Critical!')
