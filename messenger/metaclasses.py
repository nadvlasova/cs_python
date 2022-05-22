import dis

"""Мета класс для проверки корректности сервера.
clsname - экземпляр Метакласса - Server, bases - кортеж базовых классов - (), clsdict - словарь атрибутов и 
методов экземпляра класса с которым работаем."""


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []  # Список методов, которые используются в функциях класса.
        attrs = []  # Атрибуты используемые в функциях классов
        # перебираем ключи
        for func in clsdict:
            try:
                # возвращает итератор по инструкциям в предоставленной функции, методе, строке исходного кода или объекте кода.
                ret = dis.get_instructions(clsdict[func])
            # Если не функция, то ловим исключение
            except TypeError:
                pass
            # если функция, то разбираем код получая используемые методы и атрибуты.
            else:
                for i in ret:
                    print(i)
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            # заполняем список методами, использующимися в функциях класса.
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            # заполняем список атрибутами, использующимися в функциях класса.
                            attrs.append(i.argval)
        print(methods)
        # Если обнаружено использование недопустимого метода connect, то бросаем исключение.
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        # Если сокет не инициализировался константами SOCK_STREAM(TCP) AF_INET(IPv4) , тоже бросаем исключение.from
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        # Обязательно вызываем конструктор предка.
        super().__init__(clsname, bases, clsdict)


# Мета класс для проверки корректности клиентов
class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
                # если не функция, то ловим исключение
            except TypeError:
                pass
            else:
                # если функция, разбираем код, получая используемые методы.
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        # Если обнаружено использование недопустимого метода accept, listen, socket бросаем исключение
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещенного метода.')
        # Вызов get_message  или send_message из utils считаем корректным использованием сокетов
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)
