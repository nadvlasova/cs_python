""" Отображение окна с запросом имени и пароля пользователя."""

from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, \
    QLabel, qApp


class UserNameDialog(QDialog):
    """ Стартовый диалог с запросом логина и пароля пользователя."""

    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Привет!')
        self.setFixedSize(220, 135)

        self.label = QLabel('Введите имя пользователя: ', self)
        self.label.setFixedSize(200, 20)
        self.move(10, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.btn_ok = QPushButton('Начать ', self)
        self.btn_ok.move(10, 105)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(100, 105)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.label_passwd = QLabel('Введите пароль: ', self)
        self.label_passwd.setFixedSize(150, 15)
        self.label_passwd.move(10, 55)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 75)
        self.client_passwd.setEchoMode(QLineEdit.Password)

        self.show()

    def click(self):
        """ Обработчик кнопки ОК, если поле ввода не пустое, ставим флаг и
         завершаем приложение."""
        if self.client_name.text() and self.client_passwd.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()