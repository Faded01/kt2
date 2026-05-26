from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from database import Database
from table_window import TableWindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.resize(300, 200)
        self.setWindowTitle("Авторизация")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        button = QPushButton("Войти")

        layout.addWidget(QLabel("Логин"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.password_input)
        layout.addWidget(button)
        button.clicked.connect(self.login)
        self.setLayout(layout)

    def login(self):
        login_inp = self.login_input.text()
        password_inp = self.password_input.text()
        user_id = self.db.check_user(login_inp, password_inp)  # теперь возвращает id
        if user_id:
            self.window = TableWindow(user_id)
            self.window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный логин или пароль!")