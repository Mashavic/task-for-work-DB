#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.connect_data_base()
        # параметры окна
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle('Data Base')
        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(150, 40)
        self.btn.move(500, 10)
        self.btn.clicked.connect(self.upd)
        # ИД
        self.idp = QLineEdit(self)
        self.idp.resize(150, 40)
        self.idp.move(500, 60)
        self.idp.setReadOnly(True)
        # имя
        self.firstName = QLineEdit(self)
        self.firstName.resize(150, 40)
        self.firstName.move(500, 110)
        # здесь оценка
        self.lastName = QLineEdit(self)
        self.lastName.resize(150, 40)
        self.lastName.move(500, 160)
        # email
        self.mail = QLineEdit(self)
        self.mail.resize(150, 40)
        self.mail.move(500, 210)
    def connect_data_base(self):
        self.connection = psycopg2.connect(
            host = "127.0.0.1",
            user = "postgres",
            password = "qwerty123",
            database = "postgres",
        )
        self.cursor_view = self.connection.cursor()
        self.connection.autocommit = True

    def upd(self):
        self.tb.updt()
        self.idp.setText('')
        self.firstName.setText('')
        self.lastName.setText('')
        self.mail.setText('')
class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        self.setGeometry(10, 10, 400, 500)
        self.setColumnCount(4)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелча мыши в таблице

    def updt(self):
        self.clear()
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['customer_id', 'first_name', 'last_name', 'email']) # заголовки столцов
        self.wg.cursor_view.execute("SELECT * FROM customer")
        rows = self.wg.cursor_view.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()

# обработка щелчка мыши по таблице
    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.wg.idp.setText(self.item(row, 0).text())
        self.wg.firstName.setText(self.item(row, 1).text().strip())
        self.wg.lastName.setText(self.item(row, 2).text().strip())
        self.wg.mail.setText(self.item(row, 3).text().strip())

def main():
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()