#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import psycopg2
from config import host, user, password, db_name
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QApplication)


class FirstForm(QTableWidget):
    def __init__(self):
        super().__init__()
        self.connect_data_base()
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle('Data Base #start_table')
        self.setColumnCount(4)
        self.verticalHeader().hide()  # off show line table
        self.updt()
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.itemDoubleClicked.connect(self.on_cell_item_clicked)

    def connect_data_base(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.cursor_view = self.connection.cursor()

    def updt(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['customer_id', 'first_name', 'last_name', 'email'])
        self.cursor_view.execute("SELECT * FROM customer")
        rows = self.cursor_view.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem:
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()

    def on_cell_item_clicked(self, item: QTableWidgetItem):
        self.rowClick = item.row() + 1
        self.second_form = SecondForm(self.rowClick)


class SecondForm(QTableWidget):
    def __init__(self, rowClick):
        self.rowClick = rowClick  # line
        self.connect_data_base()
        super().__init__()
        self.setGeometry(400, 400, 600, 600)
        self.setWindowTitle('Data Base #end_table')
        self.setColumnCount(4)
        self.verticalHeader().hide()
        self.updt_new()
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.show()

    def connect_data_base(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.cursor_view = self.connection.cursor()
        self.connection.autocommit = True

    def updt_new(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['payment_id', 'customer_id', 'amount', 'payment_date'])
        self.cursor_view.execute("select * from payment where customer_id = {}".format(self.rowClick))
        rows = self.cursor_view.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem:
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()


def main():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE if exists customer, payment;"""
            )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE customer(
                    customer_id serial PRIMARY KEY,
                    first_name varchar(25) NOT NULL,
                    last_name varchar(25) NOT NULL,
                    email varchar(30));
                """
            )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE payment(
                    payment_id serial PRIMARY KEY,
                    customer_id integer,
                    amount real,
                    payment_date date);
                """
            )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO customer (first_name, last_name, email) VALUES
                ('Nikolay', 'Nikolaev', 'NN@test.ru');
                INSERT INTO customer (first_name, last_name, email) VALUES
                ('Vlad', 'Keep', 'Vlad@test.ru');
                INSERT INTO customer (first_name, last_name) VALUES
                ('Ivan', 'Ivanov');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (1, 8.99, '12.07.2023');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (1, 3.99, '14.07.2023');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (1, 4.99, '16.07.2023');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (2, 6.69, '13.07.2023');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (2, 7.69, '14.07.2023');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (3, 7.69, '14.07.2023');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (3, 3.69, '14.07.2023');
                INSERT INTO payment (customer_id, amount, payment_date) VALUES
                (3, 4.69, '18.07.2023');
                """
            )
        app = QApplication(sys.argv)
        window = FirstForm()
        window.show()
        sys.exit(app.exec_())


    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


if __name__ == '__main__':
    main()
