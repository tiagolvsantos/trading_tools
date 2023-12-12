import sqlite3
from sqlite3 import Error

# create_connection(r"./data/trading_tools.db")
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_update_query(query):
    conn = sqlite3.connect('./data/trading_tools.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()

def get_record_query(search_query):
    conn = sqlite3.connect('./data/trading_tools.db')
    c = conn.cursor()
    c.execute(search_query)
    return c.fetchall()
