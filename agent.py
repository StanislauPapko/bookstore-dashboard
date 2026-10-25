from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
import os
import streamlit as st

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "openai/gpt-oss-120b"
llm = ChatGroq(model = MODEL_NAME, temperature = 0)

def create_agent(db, llm = llm):
    agent = create_sql_agent(llm = llm, db=db, agent_type="tool-calling", verbose = False, handle_parsing_errors=True)
    return agent