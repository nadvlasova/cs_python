import logging

#  Базовая конфигурация

logging.basicConfig(
    filename="app_01.log",
    format="%(levelname)s %(asctime)s %(message)s",
    level=logging.INFO # ниже этого уровня писать не будет, т.е. DEBUG отсанется за бортом
)
# Для использования логгера его нужно получить(если он уже есть где-то) или создать функцией getLogger если его нет!!!
LOG = logging.getLogger('app.basic')

# Можем управлять уровнями важности
LOG.debug('Отладочная информация')  # debug не запишется т.к. 8 строка уровень-INFO
LOG.info('Информационное сообщение')
LOG.warning('Предупреждения!')
LOG.error('Ошибки')
LOG.critical('Критические сообщения!')
