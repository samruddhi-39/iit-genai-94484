
# Q1.Design a Streamlit-based application with a sidebar to switch between Groq and LM Studio. The app should accept a user question and display responses using Groq’s cloud LLM and a locally running LM Studio model.Also maintain and display the complete chat history of user questions and model responses.

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def query_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.SSLError:
        return " check your network."


def query_lm_studio(prompt):
    url = "http://127.0.0.1:1234/v1/chat/completions"

    payload = {
        "model": "microsoft/phi-4-mini-reasoning",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "LM Studio server not running. "



st.title("Groq VS LM studio chat bot: ")

st.set_page_config(page_title="Groq vs LM Studio Chat", layout="wide")


st.sidebar.title("Select Model")
model_choice = st.sidebar.radio("Choose LLM:", ["Groq Cloud", "LM Studio"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])

    with st.chat_message("assistant"):
        st.markdown(f"**{chat['model_name']}**\n\n{chat['response']}")



user_input = st.chat_input("Type your message...")

if user_input:
    
    with st.chat_message("user"):
        st.markdown(user_input)


    with st.chat_message("assistant"):
        if model_choice == "Groq Cloud":
            response = query_groq(user_input)
        else:
            response = query_lm_studio(user_input)

        st.markdown(f"**{model_choice}**\n\n{response}")

    
    st.session_state.chat_history.append({
        "user": user_input,
        "response": response,
        "model_name": model_choice
    })
