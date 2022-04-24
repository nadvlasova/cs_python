""" Простейшее логирование. Проверка работоспособности. """
import logging

LOG = logging.getLogger('app_7.log')

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

FILE_HANDLER = logging.FileHandler("app_7.log", encoding='utf-8')
FILE_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)
LOG.debug('Debug')

# Этот кусок кода с if проверка работоспособности кода написанного выше.
if __name__ == '__main__':
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setFormatter(FORMATTER)
    LOG.addHandler(STREAM_HANDLER)
    LOG.debug('Отладочное сообщение.')
