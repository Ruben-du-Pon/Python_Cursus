import streamlit as st
from functions import get_list, write_list, get_groceries, write_groceries
import os
import csv

CATEGORIES = ("Fresh Produce", "Meat & Seafood",
              "Dairy & Eggs", "Bread & Bakery",
              "Pantry Staples", "Frozen Foods",
              "Snacks & Sweets", "Beverages",
              "Condiments & Sauces",
              "Breakfast & Cereal", "Health Food",
              "Household & Cleaning Supplies",
              "Personal Care & Hygiene",
              "Pet Supplies")

midpoint = len(CATEGORIES) // 2
categories_col1 = CATEGORIES[:midpoint]
categories_col2 = CATEGORIES[midpoint:]

# Create the files if they don't exist
if not os.path.exists("./list.txt"):
    with open("./list.txt", "w") as file:
        pass
if not os.path.exists("./default_groceries.csv"):
    with open("./default_groceries.csv", "w") as file:
        header = ["category", "grocery_item"]
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow(header)
        # Add each category to the CSV
        for category in CATEGORIES:
            writer.writerow([category, ""])

# Initialize lists
grocery_list = get_list()
groceries = get_groceries()
added_groceries = []

# Set the page title, icon, and layout
st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")


# Add grocery items to the grocery list
def add_groceries():
    for grocery in added_groceries:
        if grocery not in grocery_list:
            grocery_list.append(grocery)

    write_list(grocery_list)

    # Clear checkbox state
    keys_to_clear = [key for key in st.session_state.keys() if any(
        grocery in key for grocery in added_groceries)]
    for key in keys_to_clear:
        st.session_state[key] = False

    # Clear the added_groceries list
    added_groceries.clear()


# Remove grocery items from the default grocery list
def remove_groceries():
    for grocery in added_groceries:
        for key in groceries:
            if grocery in groceries[key]:
                groceries[key].remove(grocery)
    write_groceries(groceries)
    added_groceries.clear()


# Add grocery items to the default grocery list
def add_default_groceries(category):
    if "new_grocery" in st.session_state:
        grocery = st.session_state["new_grocery"]
        if not groceries[category]:
            groceries[category] = []
        if grocery not in groceries[category]:
            groceries[category].append(grocery)
        write_groceries(groceries)


# Display the default list categories
def display_grocery_category(category, groceries):
    if category in groceries:
        anchor = category.replace(" ", "-").replace("&", "").lower()
        st.markdown(f'<h5 id="{anchor}">{category}</h5>',
                    unsafe_allow_html=True)
        for grocery in groceries[category]:
            checkbox = st.checkbox(grocery, key=f"{category}_{grocery}")
            if checkbox:
                added_groceries.append(grocery)


# Add a temporary key to detect submission
if "submit_flag" not in st.session_state:
    st.session_state["submit_flag"] = False

# Expander to show the default grocery list and add items to the current list
with st.expander(label="Add grocery item"):
    # Drop-down menu to select the category
    cat = st.selectbox("Select category", (CATEGORIES),
                       index=None, key="category",
                       placeholder="Select category")

    # Text input with on_change callback
    new_grocery_input = st.text_input(label=" ",
                                      placeholder="Add to standard grocery list",  # noqa
                                      key="new_grocery")

    # Check if the text input value has changed
    if new_grocery_input and cat and not st.session_state["submit_flag"]:
        add_default_groceries(cat)
        st.session_state["submit_flag"] = True
        st.rerun()

    # Reset the submit flag after rerun
    if st.session_state["submit_flag"]:
        st.session_state["submit_flag"] = False

    index_links = " | ".join(
        [f"[{category}](#{category.replace(' ', '-').replace('&', '').lower()})"  # noqa
         for category in CATEGORIES])
    st.markdown(index_links)

    col1, col2 = st.columns(2)
    with col1:
        # Show the first half of the default grocery list with checkboxes
        for category in categories_col1:
            display_grocery_category(category, groceries)

    with col2:
        # Show the second half of the default grocery list with checkboxes
        for category in categories_col2:
            display_grocery_category(category, groceries)

    col3, col4 = st.columns(2)
    with col3:
        st.button(label="Add to list", key="add_button",
                  on_click=add_groceries)
    with col4:
        st.button(label="Remove from standard list",
                  key="remove_button", on_click=remove_groceries)


# Display the grocery list
st.title("Groceries")

for grocery in grocery_list:
    checkbox = st.checkbox(grocery, key=grocery)
    if checkbox:
        grocery_list.remove(grocery)
        write_list(grocery_list)
        del st.session_state[grocery]
        st.rerun()
