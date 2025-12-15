# 2.
# Show Login Form. If login is successful (fake auth if username & passwd is
# same, consider valid user), show weather page. There input a city name
# from text box and display current weather information. Provide a logout
# button and on its click, display thanks message.

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MY_API")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logged_out" not in st.session_state:
    st.session_state.logged_out = False


def login_page():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password and username == password:
            st.session_state.logged_in = True
            st.session_state.logged_out = False
            st.success("Login Successful!")
        else:
            st.error("Invalid credentials")


def weather_page():
    st.title("Weather Information")

    city = st.text_input("Enter City Name :-")

    if st.button("Get Weather"):
        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                st.write(" Temperature:", data["main"]["temp"], "°C")
                st.write(" Weather:", data["weather"][0]["description"])
                st.write(" Humidity:", data["main"]["humidity"], "%")
            else:
                st.error("City not found!")
        else:
            st.warning("Please enter a city name")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logged_out = True


def thank_you_page():
    st.title("Thank You !")
    st.write("You have been logged out successfully!")


if st.session_state.logged_in:
    weather_page()
elif st.session_state.logged_out:
    thank_you_page()
else:
    login_page()
