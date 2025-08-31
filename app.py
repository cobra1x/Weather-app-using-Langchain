from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()
weather= OpenWeatherMapAPIWrapper(openweathermap_api_key=st.secrets["OPENWEATHERMAP_API_KEY"])

st.title('Weather info and suggestion for today')
input_txt=st.text_input("Enter only the city name")
india_tz=pytz.timezone("Asia/Kolkata")
today=datetime.datetime.now(india_tz)
if input_txt:
    try:
        weather_data = weather.run(input_txt)
    except Exception as e:
        st.error("Could not fetch weather data. Please check the city name and try again.")
        weather_data = None

prompt= ChatPromptTemplate.from_messages(
    [
        ("system","You are a  helpful assistant.Please response to user queries"),
        ("user",'''
           Here is the following weather conditions in the {city} {today}:
            Before that First give an intro of the city and current date and time and dont wrrite like -As of ,make it proper,then
            {weather}
            Suggest:
            1. Outdoor activities suitable for this weather
            2. Indoor alternatives if weather is restrictive
            3. Local places or experiences to explore in [Location]
            4. Tips for staying comfortable or safe in this weather
            5. Bonus: Food or drink recommendations that pair well with the weather
         ''')
    ]
)
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=st.secrets["GOOGLE_API_KEY"])
output=StrOutputParser()
chain=prompt|llm|output

if input_txt:
    st.write(chain.invoke({
        'city':input_txt,
        'today':today,
        'weather':weather_data,
    }))
