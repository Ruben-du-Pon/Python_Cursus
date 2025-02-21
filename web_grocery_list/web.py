import streamlit as st
from functions import get_list, write_list, get_groceries, write_groceries
import os
import csv

# Create the files if they don't exist
if not os.path.exists("list.txt"):
    with open("list.txt", "w") as file:
        pass
if not os.path.exists("default_groceries.csv"):
    with open("default_groceries.csv", "w") as file:
        header = ["category", "grocery_item"]
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow(header)

# Initialize lists
grocery_list = get_list()
groceries = get_groceries()
added_groceries = []

# Set the page title, icon, and layout
st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")

# Add custom CSS for in-line buttons
st.markdown("""
            <style>
                div[data-testid="stColumn"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="stColumn"] * {
                    width: fit-content !important;
                }
                div[data-testid="stMarkdownContainer"] {
                    font-size: 1rem !important;
                }
                div[data-testid="stButton"] {
                    padding: .15rem !important;
                }
                div[data-testid="stButton"] *
                    padding: .15rem !important;
                }
                div[data-testid="stBaseButton-secondary"] {
                    margin: 0 !important;
                }
                div[data-testid="stBaseButton-secondary"] *{
                    margin: 0 !important;
                }
            </style>
            """, unsafe_allow_html=True)


# Add grocery items to the grocery list
def add_groceries():
    for grocery in added_groceries:
        if grocery not in grocery_list:
            grocery_list.append(grocery)
    write_list(grocery_list)


# Remove grocery items from the default grocery list
def remove_groceries():
    for grocery in added_groceries:
        if grocery in groceries:
            del groceries[grocery]
    write_groceries(groceries)


# Add grocery items to the default grocery list
def add_default_groceries(category):
    if "new_grocery" in st.session_state:
        grocery = st.session_state["new_grocery"] + "\n"
        if not groceries[category]:
            groceries[category] = []
        if grocery not in groceries[category]:
            groceries[category].append(grocery)
        write_groceries(groceries)
        del st.session_state["new_grocery"]


# Expander to show the default grocery list and add items to the current list
with st.expander(label="Add grocery item"):
    # Drop-down menu to select the category
    cat = st.selectbox("Select category", ("Fresh Produce", "Meat & Seafood", "Dairy & Eggs", 
                                           "Bread & Bakery", "Pantry Staples", "Frozen Foods", 
                                           "Snacks & Sweets", "Beverages", "Condiments & Sauces", 
                                           "Breakfast & Cereal", "Health Food", "Household & Cleaning Supplies", 
                                           "Personal Care & Hygiene"), 
                                           index=None, key="category", placeholder="Select category")
    
    # Text input with on_change callback
    new_grocery_input = st.text_input(label=" ", placeholder="Add to standard grocery list",
                  key="new_grocery", on_change=None)  # Do not call the function immediately

    # Check if the text input value has changed
    if new_grocery_input:
        add_default_groceries(new_grocery_input)

    # Show the default grocery list with checkboxes
    for category, items in groceries.items():
        for index, grocery in enumerate(items):
            checkbox = st.checkbox(grocery, key=f"{category}_{str(index)}")
            if checkbox and grocery not in grocery_list:
                added_groceries.append(grocery)
                grocery_list.append(grocery)

    col1, col2 = st.columns(2)
    with col1:
        st.button(label="Add to list",
                  key="add_button",
                  on_click=add_groceries,)
    with col2:
        st.button(label="Remove from standard list", key="remove_button",
                  on_click=remove_groceries)


# Display the grocery list
st.title("Groceries")

for grocery in grocery_list:
    checkbox = st.checkbox(grocery, key=grocery)
    if checkbox:
        grocery_list.remove(grocery)
        write_list(grocery_list)
        del st.session_state[grocery]
        st.rerun()
