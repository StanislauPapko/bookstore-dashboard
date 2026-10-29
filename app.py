from extraction import extract
from transformation import transform_orders, transform_users, transform_books
from analytics import get_daily_price, get_unique_user_count, get_top_spender_ids, get_unique_author_count, get_most_popular_author
from unique_index import create_id_dict
import pandas as pd
from agent import create_agent
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import HumanMessage, AIMessage
from groq import RateLimitError
import streamlit as st

st.set_page_config(page_title = 'Bookstore Dashboard', layout = 'wide')

def create_store_tab(store_number:int):
    orders_path, users_path, books_path = (rf'data/STORE{store_number}/orders.parquet', rf'data/STORE{store_number}/users.csv', rf'data/STORE{store_number}/books.yaml')
    orders, users, books = extract(orders_path), extract(users_path), extract(books_path)
    orders = transform_orders(orders)
    users = transform_users(users)
    books = transform_books(books)
    daily_price = get_daily_price(orders)
    DAYS_TO_SHOW = 5
    top_revenue_days = daily_price.nlargest(DAYS_TO_SHOW, 'paid_price')
    columns = ('name', 'phone', 'address', 'email')
    id_dict = create_id_dict(users, *(columns))
    unique_user_count = get_unique_user_count(users, id_dict)
    top_spender_ids = get_top_spender_ids(orders, users, id_dict)
    unique_author_count = get_unique_author_count(books)
    most_popular_author = get_most_popular_author(orders, books)
    FIRST_RAW_COLUMNS = 4
    metric1, metric2, metric3, metric4 = st.columns(FIRST_RAW_COLUMNS)
    with metric1:
        st.metric(label = "Number of Unique Users", value=unique_user_count)
    with metric2:
        st.metric(label = "Number of Unique Author Sets", value=unique_author_count)
    with metric3:
        st.write("Most Popular Author(s)") 
        st.write(f'{most_popular_author}')
    with metric4:
        st.write("Best Buyer's IDs") 
        st.write(f'{top_spender_ids}')
    SECOND_RAW_DIVISION = [1,3]
    table, chart = st.columns(SECOND_RAW_DIVISION)
    with table:
        st.subheader("Top 5 Days by Revenue")
        st.write(top_revenue_days)   
    with chart:
        st.subheader("Daily Revenue ($)")
        st.line_chart(daily_price)
    with st.sidebar:
        st.title("AI Assistant")
        BOX_HEIGHT = 450
        messages_box = st.container(height=BOX_HEIGHT)
        history_key = f"chat_history_{store_number}"
        if history_key not in st.session_state:
            st.session_state[history_key] = []
        with messages_box:
            for message in st.session_state[history_key]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        if user_input := st.chat_input("Ask a question about the data", key=f'chat_{store_number}'):
            st.session_state[history_key].append({"role": "user", "content": user_input})
            with messages_box:
                with st.chat_message("user"):
                    st.write(user_input)
                URI_STRING = f"sqlite:///databases/store{store_number}.db"
                db = SQLDatabase.from_uri(URI_STRING) 
                agent = create_agent(db = db)      
                try:
                    with st.chat_message("assistant"):
                        history = []
                        for message in st.session_state[history_key][:-1]:
                            if message["role"] == "user":
                                history.append(HumanMessage(content=message["content"]))
                            else:
                                history.append(AIMessage(content=message["content"]))
                        answer = agent.invoke({"input": user_input, "chat_history":history})
                        st.write(answer["output"])
                        st.session_state[history_key].append({"role": "assistant", "content": answer["output"]})
                except RateLimitError:
                    st.warning("AI API rate limit reached. Please wait a moment before trying again.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

NUMBER_OF_STORES = 5
stores = [f"Store {i}" for i in range(1, NUMBER_OF_STORES + 1)]
selected_store = st.selectbox("Select store:", stores)
selected_store_number = int(selected_store.split()[-1])
create_store_tab(selected_store_number)