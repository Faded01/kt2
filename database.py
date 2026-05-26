import pymysql
from PyQt6.QtWidgets import QMessageBox


class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Dahakk0330%',
                database='izdatelskii_centre',
                cursorclass=pymysql.cursors.Cursor
            )
        except pymysql.MySQLError as e:
            QMessageBox.critical(None, "Ошибка БД", f"Ошибка подключения: {e}")

    def get_data(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
                headers = [column[0] for column in cursor.description]
            return headers, data
        except pymysql.MySQLError as e:
            QMessageBox.warning(None, "Ошибка БД", f"Ошибка запроса: {e}")
            return [], []

    def check_user(self, login, password):
        """Возвращает id_zakazchik при успешной авторизации, иначе None."""
        query = "SELECT id_zakazchik FROM zakazchiki WHERE login = %s AND password = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (login, password))
                row = cursor.fetchone()
            return row[0] if row else None
        except pymysql.MySQLError as e:
            QMessageBox.warning(None, "Ошибка БД", f"Ошибка авторизации: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()