

# Q2:
# Create a Streamlit application that takes a city name as input from the user.Fetch the current weather using a Weather API and use an LLM to explain the weather conditions in simple English.

import streamlit as st
from dotenv import load_dotenv
import os
import requests
from langchain.chat_models import init_chat_model


load_dotenv()

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not weather_api_key or not groq_api_key:
    st.error("API keys not found in environment variables")
    st.stop()


llm = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)


st.set_page_config(page_title="Weather Explainer", page_icon="🌦️")

st.title("🌦️ Weather  App")
st.write("Enter a city name to get weather data and a simple explanation.")

city = st.text_input("🏙️ Enter city name")


if st.button("Get Weather"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching weather data..."):
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={weather_api_key}&units=metric"
            )

            response = requests.get(url)

            if response.status_code != 200:
                st.error(response.json().get("message", "Error fetching weather"))
            else:
                weather_data = response.json()

                temp = weather_data["main"]["temp"]
                humidity = weather_data["main"]["humidity"]
                pressure = weather_data["main"]["pressure"]
                wind_speed = weather_data["wind"]["speed"]

                
                st.subheader(f"📊 Weather Data for {city}")
                st.write(f"🌡️ **Temperature:** {temp} °C")
                st.write(f"💧 **Humidity:** {humidity} %")
                st.write(f"🌬️ **Wind Speed:** {wind_speed} m/s")
                st.write(f"🧭 **Air Pressure:** {pressure} hPa")

                
                llm_input = f"""
                Explain the following weather data for {city} in simple English:

                Temperature  : {temp} °C
                Humidity     : {humidity} %
                Air Pressure : {pressure} hPa
                Wind Speed   : {wind_speed} m/s
                """

                with st.spinner("Generating explanation..."):
                    explanation = llm.invoke(llm_input)

                st.subheader("🧠 Weather Explanation")
                st.markdown(explanation.content)
