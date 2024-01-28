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
    df_data = pd.read_csv(r"C:\\Users\\tiago\\Downloads\\etf-constituents-01-28-2024.csv")
    search_query = "select * from data_index_constituints"
    df_search_result = pd.DataFrame(get_record_query(search_query))
    df_data.columns=["Symbol","Name"]
    for index, row in df_data.iterrows():
        if len(df_search_result) == 0 or len(df_search_result[df_search_result[0].str.contains(row["Symbol"])])==0:
            query = "insert into data_index_constituints (symbol, index) VALUES('"+row["symbol"]+"','sp500')"
            create_update_query(query)
