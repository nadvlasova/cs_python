from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import os
from common.variables import *
import datetime


# Класс - оболочка для работы с БД клиента. Использует SQLite БД, реализован с помощью SQLAlchemy (классический подход).
class ClientDatabase:
    # Класс - отображение таблицы всех известных пользователей.
    class KnownUsers:
        def __init__(self, user):
            self.id = None
            self.username = user

    # Класс - отображение для таблицы статистики переданных сообщений.
    class MessageStat:
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    # Класс - отображение списка контактов.
    class Contacts:
        def __init__(self, contact):
            self.id = None
            self.name = contact

    # Конструктор класса.
    def __init__(self, name):
        # Создаем движок БД, т.к. разрешено несколько клиентов одновременно, каждый должен иметь свою БД.
        # Т.К. Клиент мультипоточный необходимо отключить проверки на подключение с разных потоков, иначе -
        #  - sqlite3.ProgrammingError
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client_{name}.db3'
        self.database_engine = create_engine(f'sqlite:///{os.path.join(path, filename)}', echo=False,
                                             pool_recycle=7200, connect_args={'check_same_thread': False})

        # Создаем объект MetaData.
        self.metadata = MetaData()

        # Создаем таблицу известных пользователей.
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )

        # Создаем таблицу истории сообщений.
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        # Создаем таблицу контактов.
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        # Создаем таблицы.
        self.metadata.create_all(self.database_engine)

        # Создаем отображение.
        mapper(self.KnownUsers, users)
        mapper(self.MessageStat, history)
        mapper(self.Contacts, contacts)

        # Создаем сессию.
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Необходимо отчистить таблицу контактов, т.к. при запуске они подгружаются с сервера.
        self.session.query(self.Contacts).delete()
        self.session.commit()

    # Функция добавления контактов в БД.
    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    # Функция очищающая таблицу со списком контактов.
    def contacts_clear(self):
        self.session.query(self.Contacts).delete()

    # Функция удаления контакта.
    def del_contact(self, contact):
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    # Функция добавления известных пользователей.
    # Пользователи получаются только с сервера, поэтому таблица очищается.
    def add_users(self, users_list):
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    # Функция сохраняющая сообщения в БД.
    def save_message(self, contact, direction, message):
        message_row = self.MessageStat(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    # Функция возвращающая список всех контактов.
    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    # Функция возвращающая список известных пользователей.
    def get_users(self):
        return[user[0] for user in self.session.query(self.KnownUsers.username).all()]

    # Функция проверяющая наличие пользователей в известных.
    def check_user(self, user):
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    # Функция проверяющая наличие пользователя в контактах.
    def check_contact(self, contact):
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    # Функция возвращающая историю переписки с определенным пользователем.
    def get_history(self, contact):
        query = self.session.query(self.MessageStat).filter_by(contact=contact)
        return [(history_row.contact, history_row.direction, history_row.message, history_row.date)
                for history_row in query.all()]


# Отладка.
if __name__ == '__main__':
    test_db = ClientDatabase('test1')
    print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))

















