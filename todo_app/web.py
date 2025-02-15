import streamlit as st
from functions.functions import get_todos, write_todos

todos = get_todos()

st.title("Groceries")

for todo in todos:
    st.checkbox(todo)

st.text_input("")
st.button(label="save", on_click=write_todos(todos))
