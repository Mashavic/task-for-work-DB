#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import psycopg2
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QApplication, QDialog)


class Tb(QTableWidget):
    def __init__(self):
        super().__init__()
        self.connect_data_base()
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle('Data Base #start_table')
        self.setColumnCount(4)
        self.verticalHeader().hide()
        self.updt()  # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # запретить изменять поля
        # ДВОЙНОЙ КЛИК
        self.itemDoubleClicked.connect(self.on_cell_item_clicked)

    def connect_data_base(self):
        self.connection = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password="qwerty123",
            database="postgres"
        )
        self.cursor_view = self.connection.cursor()
        self.connection.autocommit = True

    def updt(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['customer_id', 'first_name', 'last_name', 'email'])  # заголовки столцов
        self.cursor_view.execute("SELECT * FROM customer")
        rows = self.cursor_view.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem:  # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()

    def on_cell_item_clicked(self):
        self.second_form = SecondForm()


class SecondForm(QTableWidget):
    def __init__(self):
        self.connect_data_base()
        super().__init__()
        self.setGeometry(400, 400, 800, 800)
        self.setWindowTitle('Вторая форма')
        self.setColumnCount(4)
        self.verticalHeader().hide()
        self.updt_new()  # обновить таблицу
        self.show()

    def connect_data_base(self):
        self.connection = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password="qwerty123",
            database="postgres"
        )
        self.cursor_view = self.connection.cursor()
        self.connection.autocommit = True

    def updt_new(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['payment_id', 'customer_id', 'amount', 'payment_date'])  # заголовки столцов
        self.cursor_view.execute("select * from payment where customer_id = {}".format(1))
        rows = self.cursor_view.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem:  # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()
def main():
    try:
        app = QApplication(sys.argv)
        window = Tb()
        window.show()
        sys.exit(app.exec_())
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


if __name__ == '__main__':
    main()