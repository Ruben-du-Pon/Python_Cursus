import streamlit as st
import functions
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

# Create files if they don't exist
if not os.path.exists("list.txt"):
    with open("list.txt", "w") as file:
        pass
if not os.path.exists("default_groceries.csv"):
    with open("default_groceries.csv", "w") as file:
        header = ["category", "grocery_items"]
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow(header)
        # Add each category to the CSV
        for category in CATEGORIES:
            writer.writerow([category, ""])

# Initialize lists
grocery_list = functions.get_list()
groceries = functions.get_groceries()
added_groceries = []

# Set the page title, icon, and layout
st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")


# Clear the session state
def clear_session_state():
    keys_to_clear = [key for key in st.session_state.keys() if any(
        grocery.strip() in key for grocery in added_groceries)]
    for key in keys_to_clear:
        st.session_state[key] = False


# Add grocery items to the grocery list
def add_groceries():
    for grocery in added_groceries:
        if grocery not in grocery_list:
            grocery_list.append(grocery.title())

    functions.write_list(grocery_list)
    clear_session_state()
    added_groceries.clear()


# Remove grocery items from the default grocery list
def remove_groceries():
    for grocery in added_groceries:
        for key in groceries:
            if grocery.strip() in groceries[key]:
                groceries[key].remove(grocery.strip())
    functions.write_groceries(groceries)
    added_groceries.clear()


# Add grocery items to the default grocery list
def add_default_groceries(category):
    if "new_grocery" in st.session_state:
        grocery = st.session_state["new_grocery"]
        if not groceries[category]:
            groceries[category] = []
        if grocery not in groceries[category]:
            groceries[category].append(grocery.title())
        functions.write_groceries(groceries)


# Display the default list categories
def display_grocery_category(category, groceries):
    if category in groceries:
        # Clean up the category name for the anchor
        anchor = functions.clean_category_name(category)

        # Display the category name
        st.markdown(f'<h5 id="{anchor}">{category}</h5>',
                    unsafe_allow_html=True)

        # Display the grocery items
        for grocery in groceries[category]:
            checkbox = st.checkbox(grocery, key=f"{category}_{grocery}")
            if checkbox:
                added_groceries.append(grocery + "\n")


# Process the grocery input
def process_grocery_input():
    cat = st.session_state.get("category", None)
    grocery = st.session_state.get("tmp_grocery", "").strip()

    if not grocery:
        return

    if cat not in CATEGORIES:
        st.error("Please select a category")
        return

    st.session_state["new_grocery"] = grocery
    add_default_groceries(cat)
    st.session_state["tmp_grocery"] = ""


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
                                      on_change=process_grocery_input)

    # Check if a category has been selected
    if new_grocery_input:
        if cat not in CATEGORIES:
            st.error("Please select a category")
            st.stop()
        add_default_groceries(cat)
        st.rerun()

    # Links to navigate the categories
    index_links = " | ".join([
        f"[{category}](#{functions.clean_category_name(category)})"
        for category in CATEGORIES])
    st.markdown(index_links)

    # Add custom CSS for mobile-friendly layout
    st.markdown("""
            <style>
                /* Make fonts smaller on mobile devices */
                @media (max-width: 600px) {
                    h5 {
                        font-size: 1.1rem !important;
                    }
                    .css-1s9bf49 {
                        font-size: 1rem !important;
                    }
                    .css-15z7xkx {
                        font-size: 1rem !important;
                    }
                    .css-1v0mbdj {
                        font-size: 1rem !important;
                    }
                }

                /* Index links styling for mobile */
                @media (max-width: 600px) {
                    .css-13wxj5s {
                        font-size: 0.9rem !important;
                        display: block;
                        padding: 5px;
                        line-height: 1.2;
                    }
                }

                /* Adjust container width */
                .container {
                    max-width: 100% !important;
                }
            </style>
        """, unsafe_allow_html=True)

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
        functions.write_list(grocery_list)
        del st.session_state[grocery]
        st.rerun()
