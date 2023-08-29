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
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchone()}")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE c(
                    id serial PRIMARY KEY,
                    first_name varchar(50) NOT NULL,
                    second_name varchar(50) NOT NULL);
                """
            )
            print("[INFO] Table created successfull")
    except:
        print("[INFO] Table exist")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO students (first_name, second_name) VALUES
            ('Ivan', 'Ivanov'),
            ('Nikolay', 'Nikolaev');
            """
        )




except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
