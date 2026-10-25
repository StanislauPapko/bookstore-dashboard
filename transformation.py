import numpy as np
import pandas as pd

EXCHANGE_RATE = 1.2
def standardize_price(price:str) -> float:
    if '$' in price or 'USD' in price: 
        return float(price.replace('$', '').replace('¢', '').replace('USD', ''))
    elif '€' in price or 'EUR' in price:
        return round(float(price.replace('€', '').replace('¢', '').replace('EUR', '')) * EXCHANGE_RATE, 2)
    else:
        raise ValueError("Unrecognised currency")

def timestamp_to_date(orders, timestamp_col:str = 'timestamp'):
    orders[timestamp_col] = orders[timestamp_col].str.replace(',', ' ').str.replace('A.M.', 'AM').str.replace('P.M.', 'PM')
    return pd.to_datetime(orders[timestamp_col], format='mixed').dt.date

def transform_orders(orders, price_col:str = 'unit_price', quantity_col:str = 'quantity', timestamp_col:str = 'timestamp', shipping_col:str = 'shipping'):
    orders['date'] = timestamp_to_date(orders)
    orders[price_col] = np.vectorize(standardize_price)(orders[price_col])
    orders['paid_price'] = orders[price_col] * orders[quantity_col]
    orders = orders.drop([timestamp_col, shipping_col], axis = 1)
    return orders

FILLNA_STRING = 'Unknown'
def transform_users(users, id_col:str = 'user_id', name_col:str = 'name', address_col:str = 'address', phone_col:str = 'phone', email_col:str = 'email'):
    users.columns = [id_col, name_col, address_col, phone_col, email_col]
    users[address_col] = np.vectorize(lambda x: FILLNA_STRING if x.strip() == '' else x)(users[address_col].fillna(FILLNA_STRING))
    return users

def transform_books(books, id_col:str = 'book_id', title_col:str = 'title', author_col:str = 'author', genre_col:str = 'genre', publisher_col:str = 'publisher', year_col:str = 'year'):
    books.columns = [id_col,title_col,author_col,genre_col,publisher_col,year_col]
    books[publisher_col] = books[publisher_col].fillna(FILLNA_STRING)
    books[year_col] = pd.to_numeric(books[year_col], errors='coerce').astype('Int64')
    return books