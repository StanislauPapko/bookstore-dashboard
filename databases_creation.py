from extraction import extract
from transformation import transform_orders, transform_users, transform_books
from loading import load
from unique_index import create_id_dict

NUMBER_OF_STORES = 5
for i in range(1, NUMBER_OF_STORES+1):
    store_dir = f'STORE{i}'
    db_filename = f'store{i}.db'
    db_path = rf'databases\{db_filename}'
    orders_path, users_path, books_path = (rf'data\{store_dir}\orders.parquet', rf'data\{store_dir}\users.csv', rf'data\{store_dir}\books.yaml')
    orders, users, books = extract(orders_path), extract(users_path), extract(books_path)
    orders = transform_orders(orders)
    users = transform_users(users)
    books = transform_books(books)
    load(orders, db_path, 'orders')
    load(users, db_path, 'users')
    load(books, db_path, 'books')