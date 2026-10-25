import numpy as np
import pandas as pd

def get_daily_price(orders, date_col:str = 'date', price_col:str = 'paid_price'):
    return orders[[price_col, date_col]].groupby(date_col).sum()

def get_unique_user_count(users, id_dict:dict, original_id:str = 'user_id') -> int:
    users['new_id'] = users[original_id].map(id_dict)
    return users['new_id'].nunique()

def get_top_spender_ids(orders, users, id_dict:dict, id_in_orders:str = 'user_id', id_in_users:str = 'user_id', price_col:str = 'paid_price') -> list:
    orders['new_user_id'] = orders[id_in_orders].map(id_dict)
    top_spender_id = orders.groupby('new_user_id')[price_col].sum().idxmax()
    return users[users['new_id'] == top_spender_id][id_in_users].tolist()

def get_author_set(author : str) -> frozenset:
    return frozenset(author.split(', '))

def get_unique_author_count(books, author_col:str = 'author') -> int:
    return len(set(np.vectorize(get_author_set)(books[author_col])))

def get_most_popular_author(orders, books, id_col:str = 'book_id', quantity_col:str = 'quantity', author_col:str = 'author') -> str:
    return pd.merge(orders[[id_col, quantity_col]], books[[id_col, author_col]], on=id_col).groupby(author_col)[quantity_col].sum().idxmax()