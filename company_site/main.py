import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("The Best Company")

content1 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit 
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint 
occaecat cupidatat non proident, sunt in culpa qui officia 
deserunt mollit anim id est laborum.
"""  # noqa

st.write(content1)

st.header("Our Team")
team = pd.read_csv("data.csv")


def write_team_member(row):
    st.subheader(row["first name"].capitalize() +
                 " " + row["last name"].capitalize())
    st.write(row["role"])
    st.image("images/" + row["image"])


col1, col2, col3 = st.columns(3)
with col1:
    for index, row in team[0::3].iterrows():
        write_team_member(row)

with col2:
    for index, row in team[1::3].iterrows():
        write_team_member(row)

with col3:
    for index, row in team[2::3].iterrows():
        write_team_member(row)
