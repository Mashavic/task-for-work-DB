import psycopg2
from config import host, user, password, db_name

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
        print("[INFO] Deleted tables successfully")

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
        print("[INFO] Table created successfull")

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
        print("[INFO] Table created successfull")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO customer (first_name, last_name, email) VALUES
            ('Nikolay', 'Nikolaev', 'NN@test.ru');
            INSERT INTO customer (first_name, last_name) VALUES
            ('Ivan', 'Ivanov');
            INSERT INTO payment (customer_id, amount, payment_date) VALUES
            (1, 8.99, '12.07.2023');
            INSERT INTO payment (customer_id, amount, payment_date) VALUES
            (1, 6.69, '13.07.2023');
            """
        )
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                customer.customer_id,
                first_name,
                last_name,
                email,
                amount,
                payment_date
            FROM
                customer
            INNER JOIN payment ON payment.customer_id = customer.customer_id;
            """
        )



except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
