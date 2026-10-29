from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import streamlit as st

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "openai/gpt-oss-120b"
llm = ChatGroq(model = MODEL_NAME, temperature = 0, max_retries = 0)
prompt = ChatPromptTemplate.from_messages([
    ("system", '''You are an AI data assistant for a bookstore.
                You can have normal conversations and answer general questions.
                Use the SQL database tools only when the user specifically asks for data or metrics.
                Use the provided chat history to understand the context.'''),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")])

def create_agent(db, llm = llm, prompt=prompt):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True, max_iterations=4)
    return agent_executor