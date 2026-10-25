import pandas as pd
import sqlite3

def load(df, db_path:str, table_name:str):
    connection = sqlite3.connect(db_path)
    df.to_sql(table_name, connection, index=False, if_exists="replace")
    connection.close()