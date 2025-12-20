import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

st.set_page_config(page_title="LangChain Agent Demo", layout="wide")
st.title("LangChain Agent Streamlit Chat")


# Tools

@tool
def calculator(expression):
    """Evaluate an arithmetic expression (+, -, *, /, parentheses)."""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error : cannot solve expression"

@tool
def get_weather(city):
    """Fetch current weather for a given city using OpenWeather API."""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return f"API Error: {data}"
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        return f"Temperature: {temp}°C, Humidity: {humidity}%, Wind Speed: {wind} m/s"
    except Exception as e:
        return f"Error: {e}"

@tool
def read_file(filepath):
    """Read and return the contents of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except Exception as e:
        return f"Error reading file: {e}"


# Middleware

@wrap_model_call
def model_logging(request, handler):
    st.write("--- BEFORE MODEL CALL ---")
    response = handler(request)
    st.write("--- AFTER MODEL CALL ---")
    if response.result and response.result[0].content:
        response.result[0].content = response.result[0].content.upper()
    return response


llm = init_chat_model(
    model="google/gemma-3n-e4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)

agent = create_agent(
    model=llm,
    tools=[calculator, get_weather, read_file],
    middleware=[model_logging],
    system_prompt="You are a helpful assistant. Answer in short. Always use the calculator tool for arithmetic expressions."
)

# Session state

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None



user_input = st.text_input("You:", key="input_text")

if st.button("Send") and user_input:

    st.session_state.chat_history.append({"user": user_input})

    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    st.session_state.last_result = result

   
    ai_msg = result["messages"][-1].content
    st.session_state.chat_history.append({"ai": ai_msg})


for chat in st.session_state.chat_history:
    if "user" in chat:
        st.markdown(f"**You:** {chat['user']}")
    if "ai" in chat:
        st.markdown(f"**AI:** {chat['ai']}")


if st.checkbox("Show raw message history"):
    if st.session_state.last_result:
        st.json([msg.content for msg in st.session_state.last_result["messages"]])
    else:
        st.info("No messages yet. Send a message first.")
