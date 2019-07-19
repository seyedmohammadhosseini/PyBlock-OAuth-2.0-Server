# Following are important sqlite3 module routines, which can suffice your requirement to work with SQLite database.
# SQLite is a C library that provides a lightweight disk-based database that doesn’t require a separate server process
# and allows accessing the database using a nonstandard variant of the SQL query language. Some applications can use
# SQLite for internal data storage. It’s also possible to prototype an application using SQLite and then port the code
# to a larger database such as PostgreSQL or Oracle.
# https://docs.python.org/3/library/sqlite3.html

import sqlite3
from sqlite3 import Error


class controller:

    # Initialize the database class
    # :param register: access to all other class
    def __init__(self, register):
        self.register = register
        pass

    # create a database connection to a SQLite database
    # This API opens a connection to the SQLite database file. t returns a connection object.
    @staticmethod
    def connection(db_file):
        # Parameters
        # db_file :: database file path
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print("Database Error :: " + e)
            exit(1)
        # finally:
        #    conn.close()

    # create a database connection to a database that resides in the memory
    # You can use ":memory:" to open a database connection to a database that resides in RAM instead of on disk.
    # If database is opened successfully, it returns a connection object.
    @staticmethod
    def memoryConnection():
        try:
            conn = sqlite3.connect(':memory:')
        except Error as e:
            print("Memory Database Error :: " + e)
        # finally:
        #    conn.close()

    # create a table from the create_table_sql statement
    # :param conn: Connection object
    # :param create_table_sql: a CREATE TABLE statement
    @staticmethod
    def createTable(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print("Create Table Error :: " + e)
            exit(1)

    # Create a new project into the projects table
    # :param conn:
    # :param project:
    # :return: last insert id
    @staticmethod
    def insert(conn, query, data):
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return cur.lastrowid

    # update priority, begin_date, and end date of a task
    # :param conn:
    # :param task:
    @staticmethod
    def update(conn, query, data):
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()

    # Select Records
    # :param conn: the Connection object
    # :param priority:
    # :return: array
    @staticmethod
    def select(conn, query, data):
        cur = conn.cursor()
        cur.execute(query, data)
        rows = cur.fetchall()
        result = []
        for row in rows:
            temp = []
            for a in row:
                temp.append(a)
            result.append(temp)
        return result
