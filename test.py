#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem)

class Tb(QTableWidget):
    def __init__(self):
        super().__init__()
        self.connect_data_base()
        self.setGeometry(10, 10, 400, 500)
        self.setWindowTitle('Data Base')
        self.setColumnCount(4)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля

    def connect_data_base(self):
        self.connection = psycopg2.connect(
            host = "127.0.0.1",
            user = "postgres",
            password = "qwerty123",
            database = "postgres",
        )
        self.cursor_view = self.connection.cursor()
        self.connection.autocommit = True
    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['customer_id', 'first_name', 'last_name', 'email']) # заголовки столцов
        self.cursor_view.execute("SELECT * FROM customer")
        rows = self.cursor_view.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()


def main():
    app = QApplication(sys.argv)
    window = Tb()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()