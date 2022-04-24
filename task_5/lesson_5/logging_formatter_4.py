""" Установка уровня в обработчике (STREAM_HANDLER.setLevel(logging.CRITICAL))
имеет приоритет выше чем установка уровня в регистраторе(APP_LOG.setLevel(logging.DEBUG))!!!!!!"""

import logging
import sys

APP_LOG = logging.getLogger('app')
APP_LOG.setLevel(logging.DEBUG)

STREAM_HANDLER = logging.StreamHandler(sys.stderr)  # Этот обработчик с уровнем CRITICAL выводит сообщение в консоль
STREAM_HANDLER.setLevel(logging.CRITICAL)

FILE_HANDLER = logging.FileHandler('app_4.log')  # А этот обработчик с уровнем DEBUG выводит сообщение в файл
FILE_HANDLER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

APP_LOG.addHandler(STREAM_HANDLER)
APP_LOG.addHandler(FILE_HANDLER)

APP_LOG.debug('Debug')
APP_LOG.warning('Warning')
APP_LOG.critical('Critical')
