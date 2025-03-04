from supabase import create_client
import streamlit as st
from typing import Any
from config import FILEPATH, CATEGORIES
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)


# Core File Operation Functions
def get_list(filepath: str = FILEPATH) -> list[str]:
    """
    Read a text file and return each line as a grocery list.

    Keyword Arguments:
        filepath -- The file to read (default: {"list.txt"})

    Returns:
        A grocery list
    """
    with open(filepath, 'r') as file_local:
        list_local = file_local.readlines()

    list_local = [item.strip().title() for item in list_local]
    return list_local


def write_list(grocery_list: list[str],
               filepath: str = FILEPATH) -> None:
    """
    Write the items in the grocery_list to a file
    Arguments:
        grocery_list -- A List of to-do items to write to a file

    Keyword Arguments:
        filepath -- The file to write the list to (default: {"list.txt"})

    Returns:
        None
    """
    with open(filepath, 'w') as file_local:
        for item in grocery_list:
            # Add newline if it's not already there
            if not item.endswith("\n"):
                item += "\n"
            file_local.write(item)


def get_groceries() -> dict[str, list]:
    """
    Read a CSV file and return a dictionary with categories as keys and lists of grocery items as values.

    Returns:
        A dictionary with categories as keys and lists of grocery items as values.
    """  # noqa
    response = supabase.table('default_groceries').select("*").execute()
    print(response.data)
    return response.data[0] if response.data else {}


def write_groceries(groceries: dict[str, list]) -> None:
    """
    Write the groceries dictionary to a supabase table.

    Arguments:
        groceries -- A dictionary with categories as keys and lists of grocery items as values.

    Returns:
        None
    """  # noqa
    supabase.table('default_groceries').upsert({
        'id': 1,  # Use a constant ID for the single record
        'groceries': groceries
    }).execute()


# Grocery Management Functions
def add_default_groceries(category: str, session_state: dict[str, Any],
                          groceries: dict[str, list]) -> None:
    """
    Add a new grocery item to the default grocery list

    Arguments:
        category -- The category name
        session_state -- The Streamlit session state
        groceries -- The dictionary of grocery categories and items

    Returns:
        None
    """
    if "new_grocery" in session_state:
        grocery = session_state["new_grocery"]
        if not groceries[category]:
            groceries[category] = []
        if grocery not in groceries[category]:
            groceries[category].append(grocery.title())
        write_groceries(groceries)


def remove_groceries(groceries: dict[str, list],
                     added_groceries: list[str]) -> None:
    """
    Remove grocery items from the default grocery list.

    Arguments:
        groceries -- The dictionary of grocery categories and items
        added_groceries -- The list of added groceries

    Returns:
        None
    """
    for grocery in added_groceries:
        for key in groceries:
            if grocery.strip() in groceries[key]:
                groceries[key].remove(grocery.strip())
    write_groceries(groceries)
    added_groceries.clear()


def process_grocery_input(session_state: dict[str, Any],
                          groceries: dict[str, list],
                          categories: list = CATEGORIES) -> None:
    """
    Process the grocery input and add it to the default grocery list

    Arguments:
        session_state -- The Streamlit session state dictionary
        CATEGORIES: List of valid grocery categories
        groceries: Dictionary mapping categories to their grocery items

    Returns:
        None
    """
    cat = session_state.get("category", None)
    grocery = session_state.get("tmp_grocery", "").strip()

    if not grocery:
        return

    if cat not in categories:
        st.error("Please select a category")
        return

    session_state["new_grocery"] = grocery
    add_default_groceries(cat, session_state, groceries)
    session_state["tmp_grocery"] = ""
    st.rerun()


# UI Display Functions
def display_grocery_category(category: str, groceries: dict[str, list],
                             added_groceries: list[str]) -> None:
    """
    Display the grocery category and items as checkboxes

    Arguments:
        category -- The category name to display
        groceries: Dictionary mapping categories to their grocery items
        added_groceries: List to store selected grocery items

    Returns:
        None
    """
    if category in groceries:
        # Clean up the category name for the anchor
        anchor = clean_category_name(category)

        # Display the category name with "Back to Top" link
        st.markdown(
            f'''
            <div style="display: flex;
            justify-content: space-between;
            align-items: center;">
                <h5 style="margin: 0;" id="{anchor}">{category}</h5>
                <a href="#top" style="font-size: 0.8em;
                text-decoration: none;">Back to Top</a>
            </div>
            ''',
            unsafe_allow_html=True
        )

        # Display the grocery items
        for grocery in groceries[category]:
            checkbox = st.checkbox(grocery, key=f"{category}_{grocery}")
            if checkbox:
                added_groceries.append(grocery)


def split_categories(groceries: dict[str, list],
                     categories: list = CATEGORIES):
    """
    Split categories into two columns based on total items.

    Arguments:
        categories -- List of category names
        groceries -- Dictionary of groceries with category names as keys

    Returns:
        Two lists of categories for two columns.
    """
    print(groceries)
    total_items = sum(len(groceries[cat]) for cat in categories)
    target_items = total_items // 2

    current_items = 0
    col1_categories = []

    for category in categories:
        items_in_category = len(groceries[category])
        if current_items < target_items:
            col1_categories.append(category)
            current_items += items_in_category
        else:
            break

    col2_categories = [cat for cat in categories if cat not in col1_categories]
    return col1_categories, col2_categories


# Utility Functions
def clear_session_state(session_state: dict[str, Any],
                        added_groceries: list[str]) -> None:
    """
    Clear the session state for added groceries.

    Arguments:
        session_state -- The Streamlit session state dictionary
        added_groceries -- List of grocery items that were added

    Returns:
        None
    """
    keys_to_clear = [key for key in session_state.keys() if any(
        grocery.strip() in key for grocery in added_groceries)]
    for key in keys_to_clear:
        session_state[key] = False


def clean_category_name(category: str) -> str:
    """
    Clean the category name to be used as a URL path.

    Arguments:
        category: The category name to clean

    Returns:
        str: A cleaned category name with lowercase letters,
             hyphens instead of spaces, and no ampersands

    Example:
        >>> clean_category_name("Dairy & Eggs")
        'dairy-eggs'
    """
    category = category.lower()
    category = category.replace(" ", "-")
    category = category.replace("&", "")
    category = category.replace("--", "-")
    return category
