import streamlit as st
from functions import get_list, write_list, get_groceries, write_groceries
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


def add_groceries():
    for grocery in groceries:
        if grocery not in grocery_list:
            grocery_list.append(grocery)
    write_list(grocery_list)
    st.rerun()


def add_default_groceries():
    grocery = st.session_state["new_grocery"] + "\n"
    groceries.append(grocery)
    write_groceries(groceries)
    del st.session_state["new_grocery"]
    st.rerun()


with st.expander(label="Add grocery item"):
    st.text_input(label=" ", placeholder="Add to standard grocery list",
                  on_change=add_default_groceries, key="new_grocery")
    for grocery in groceries:
        checkbox = st.checkbox(grocery, key=grocery)
        if checkbox:
            grocery_list.append(grocery)

    st.button(label="Add", key="add_button", on_click=add_groceries)


st.title("Groceries")

for grocery in grocery_list:
    checkbox = st.checkbox(grocery, key=grocery)
    if checkbox:
        grocery_list.remove(grocery)
        write_list(grocery_list)
        del st.session_state[grocery]
        st.rerun()
