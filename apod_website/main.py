import requests
import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_KEY")
url = "https://api.nasa.gov/planetary/apod?api_key=" + api_key

response = requests.get(url)
content = response.json()

st.title("NASA Astronomy Picture of the Day")
st.subheader(content["title"])
st.image(content["hdurl"])
st.write(content["explanation"])
