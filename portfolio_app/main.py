import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)

with col1:
    st.image("images/photo.jpg")

with col2:
    st.title("Ruben du Pon")
    content = """
    Hi, this is some text about me. I am a data scientist and I love to code.
    """
    st.info(content)

content2 = """
Below you can find some of the projects I have made.
Feel free to contact me!
"""
st.write(content2)

df = pd.read_csv("data/data.csv", sep=";")

col3, col4 = st.columns(2)

with col3:
    for index, row in df[0::2].iterrows():
        st.header(row["title"])
        st.write(row["description"])
        st.image(row["image"])

with col4:
    for index, row in df[1::2].iterrows():
        st.header(row["title"])
        st.write(row["description"])
        st.image(row["image"])
