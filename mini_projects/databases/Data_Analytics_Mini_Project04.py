import sqlite3

def create_connection():
    try:
        conn = sqlite3.connect('YouTube.db')
        print('Connection successful')
        return conn
    except:
        print('Error connecting to database')

def create_table(conn, stmt):
    try:
        cursor = conn.cursor()
        cursor.execute(stmt)
        conn.commit()
        print('Table created')
    except:
        print('Unable to create table')

def populate_table(conn, stmt, entry):
    try:
        cursor = conn.cursor()
        cursor.execute(stmt, entry)
        conn.commit()
        print('Insertion successful')
    except:
        print('Unable to insert into table')

conn = create_connection()
# Read data from .csv file
