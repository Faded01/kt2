from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from database import Database


class TableWindow(QMainWindow):
    def __init__(self, user_id: int):
        super().__init__()
        self.resize(1000, 600)
        self.setWindowTitle("Издательский центр")
        self.db = Database()
        self.user_id = user_id  # id авторизованного заказчика
        self.tabs = QTabWidget()
        self.tables = {
            "Мои заказы":  f"SELECT * FROM v_zakazchik_orders WHERE zakazchik_id = {self.user_id}"
        }
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        for tab_name, query in self.tables.items():
            try:
                table = QTableWidget()
                headers, data = self.db.get_data(query)
                table.setColumnCount(len(headers))
                table.setHorizontalHeaderLabels(headers)
                table.setRowCount(len(data))
                for row_index, row in enumerate(data):
                    for col_index, value in enumerate(row):
                        item = QTableWidgetItem(str(value) if value is not None else "")
                        table.setItem(row_index, col_index, item)
                table.resizeColumnsToContents()
                self.tabs.addTab(table, tab_name)
            except Exception as error:
                QMessageBox.warning(
                    self,
                    "Ошибка загрузки таблицы",
                    f"{tab_name}\n{error}"
                )
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

    def closeEvent(self, event):
        self.db.close()
        event.accept()