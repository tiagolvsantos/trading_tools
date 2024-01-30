import sqlite3
import pandas as pd
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


def get_stock_symbols_list():
    return get_record_query("select * from tradfi_stocks_symbols")

def get_crypto_symbols_list():
    return get_record_query("select * from crypto_asset_symbols")


def insert_from_csv():
    df_data = pd.read_csv(r"C:\\Users\\User\\Downloads\\etf-constituents-01-29-2024.csv")
    df_data.columns=["Symbol","Name"]
    for index, row in df_data.iterrows():
        query = "insert into data_index_constituints (symbol, indx) VALUES('"+row["Symbol"]+"','nasdaq100')"
        create_update_query(query)
