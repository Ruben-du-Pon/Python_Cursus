import streamlit as st
import functions
import os
from config import CATEGORIES, FILEPATH
from styles import MOBILE_STYLES


# Set the page title, icon, and layout
st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")

# Add an anchor point at the top
st.markdown('<div id="top" style="position: absolute; top: 0;"></div>',
            unsafe_allow_html=True)

# Create files if they don't exist
if not os.path.exists(FILEPATH):
    with open(FILEPATH, "w") as file:
        pass

# Initialize lists
grocery_list = functions.get_list()
groceries = functions.get_groceries()
added_groceries = []
categories_col1, categories_col2 = functions.split_categories(groceries)


def add_groceries() -> None:
    """
    Add grocery items to the grocery list.

    Arguments:
        added_groceries -- The list of added groceries
        grocery_list -- The grocery list
        session_state -- The Streamlit session state
    """
    for grocery in added_groceries:
        if grocery not in grocery_list:
            grocery_list.append(grocery.title())

    functions.write_list(grocery_list)
    functions.clear_session_state(st.session_state, added_groceries)
    added_groceries.clear()


# Expander to show the default grocery list and add items to the current list
with st.expander(label="Add grocery item"):
    # Drop-down menu to select the category
    cat = st.selectbox("Select category", (CATEGORIES),
                       index=None, key="category",
                       placeholder="Select category")

    # Text input to add a new grocery item
    new_grocery_input = st.text_input(label=" ",
                                      placeholder="Add to standard grocery list",  # noqa
                                      key="tmp_grocery",
                                      on_change=functions.process_grocery_input(st.session_state, groceries))  # noqa

    # Check if a category has been selected
    if new_grocery_input:
        if cat not in CATEGORIES:
            st.error("Please select a category")
            st.stop()
        functions.add_default_groceries(cat, st.session_state, groceries)
        st.rerun()

    # Links to navigate the categories
    index_links = " | ".join([
        f"[{category}](#{functions.clean_category_name(category)})"
        for category in CATEGORIES])
    st.markdown(index_links)

    # Add custom CSS for mobile-friendly layout
    st.markdown(MOBILE_STYLES, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # Show the first half of the default grocery list with checkboxes
        for category in categories_col1:
            functions.display_grocery_category(
                category, groceries, added_groceries)

    with col2:
        # Show the second half of the default grocery list with checkboxes
        for category in categories_col2:
            functions.display_grocery_category(
                category, groceries, added_groceries)

    col3, col4 = st.columns(2)
    with col3:
        st.button(label="Add to list", key="add_button",
                  on_click=add_groceries)
    with col4:
        st.button(label="Remove from standard list",
                  key="remove_button",
                  on_click=functions.remove_groceries,
                  args=(groceries, added_groceries))


# Display the grocery list
st.title("Groceries")

for grocery in grocery_list:
    checkbox = st.checkbox(grocery, key=grocery)
    if checkbox:
        grocery_list.remove(grocery)
        functions.write_list(grocery_list)
        del st.session_state[grocery]
        st.rerun()
