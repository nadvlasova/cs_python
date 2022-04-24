

import logging
import sys

WORD = 'CRITICAL'
len(WORD)

print('{:<9}#text'.format(WORD))  # Правый отступ равен 9 - длина слово. Таким образом мы имеем 1 пробел м/у словом и решёткой???

LOG = logging.getLogger('my_logger')
STREAM_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter('%(levelname)-9s#text')
STREAM_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(STREAM_HANDLER)
LOG.setLevel(logging.CRITICAL)

LOG.critical('Критическое сообщение!')
