""" Расширенная настройка. Форматирование. Обработчики."""

import sys
import logging

# Создать или получить логгер - регистратор верхнего уровня.
LOG = logging.getLogger('basic')

"""Создать обработчик, который выводит сообщения в поток stderr
обработчики позволяют переопределять поведение корневого регистратора -log. """

CRIT_HAND = logging.StreamHandler()  # Выводит в поток сообщения с уровнем CRITICAL в консоль(можно в файл, сокет...)
# CRIT_HAND.setLevel(logging.CRITICAL)  # Установленный тут уровень будет в приоритете над установленными ниже

""" Создать объект Formatter. Определить формат сообщений."""
FORMATTER = logging.Formatter("%(levelname)-10s %(asctime)-20s %(message)s") # -10s это отступы

""" Подключить объект Formatter к обработчику. """
CRIT_HAND.setFormatter(FORMATTER)

""" Добавить обработчить к регистратору. """
LOG.addHandler(CRIT_HAND)
LOG.setLevel(logging.DEBUG) # DEBAG т.е. с какого уровня будем им управлять

""" Передать сообщение обработчику. """
LOG.info('Информационное сообщение')
LOG.critical('Конец!')


