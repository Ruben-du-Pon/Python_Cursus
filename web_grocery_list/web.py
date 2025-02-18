import streamlit as st
from functions import get_list, write_list, get_groceries
import os

# Create the files if they don't exist
if not os.path.exists("list.txt"):
    with open("list.txt", "w") as file:
        pass
if not os.path.exists("default_groceries.txt"):
    with open("default_groceries.txt", "w") as file:
        pass

grocery_list = get_list()
groceries = get_groceries()

with st.expander("Add grocery item"):
    for grocery in groceries:
        checkbox = st.checkbox(grocery, key=grocery)
        if checkbox:
            grocery_list.append(grocery)
            write_list(grocery_list)


def add_groceries():
    grocery = st.session_state["new_grocery"] + "\n"
    grocery_list.append(grocery)
    write_list(grocery_list)


st.title("Groceries")

for grocery in grocery_list:
    checkbox = st.checkbox(grocery, key=grocery)
    if checkbox:
        grocery_list.remove(grocery)
        write_list(grocery_list)
        del st.session_state[grocery]
        st.rerun()

st.text_input(label=" ", placeholder="Add grocery item",
              on_change=add_groceries, key="new_grocery")
