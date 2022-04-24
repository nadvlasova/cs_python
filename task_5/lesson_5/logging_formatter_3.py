""" Расширенная настройка. Форматирование, обработчики, задаем level регистратору и обработчику. """

import logging
# Создать логгер(LOG) - регистратор верхнего уровня с именем app.main
LOG = logging.getLogger('app.main')

# Создать обработчик(FILE_HANDLER) - запись в файл. Может быть несколько обработчиков у одного регистратора.
FILE_HANDLER = logging.FileHandler("app.log", encoding='utf-8')

# Устанавливаем уровень с которого будет работать обработчик.
FILE_HANDLER.setLevel(logging.INFO)

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

FILE_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

LOG.debug('Debug')
LOG.info('Info')
LOG.warning('Warning')
LOG.critical('Critical')
