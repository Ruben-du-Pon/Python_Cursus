import pandas as pd

FILEPATH = "list.txt"
DEFAULT_GROCERIES = "default_groceries.csv"


def get_list(filepath: str = FILEPATH) -> list[str]:
    """Read a text file and return each line as a grocery list.

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
    """Write the items in the grocery_list to a file
    Arguments:
        grocery_list -- A List of to-do items to write to a file

    Keyword Arguments:
        filepath -- The file to write the list to (default: {"list.txt"})
    """
    with open(filepath, 'w') as file_local:
        file_local.writelines(grocery_list)


def get_groceries(filepath: str = DEFAULT_GROCERIES) -> dict[str, list]:
    """Read a CSV file and return a dictionary with category names as keys 
    and lists of grocery items as values.

    Arguments:
        filepath -- The file to read

    Returns:
        A dictionary with categories as keys and lists of grocery items as values.
    """  # noqa
    df = pd.read_csv(filepath, sep=";", dtype=str)

    groceries = {}
    for _, row in df.iterrows():
        category = row["category"]
        items_str = row["grocery_items"]

        # If there are grocery items, split them by commas
        if pd.notna(items_str) and items_str.strip():
            items_list = [item.strip()
                          for item in items_str.split(",")
                          if item.strip()]
            groceries[category] = sorted(items_list)
            groceries[category] = [item.title()
                                   for item in groceries[category]]
        else:
            groceries[category] = []

    return groceries


def write_groceries(grocery_list: dict[str, list],
                    filepath: str = DEFAULT_GROCERIES) -> None:
    """Write the items in the grocery_list to a CSV file.

    Arguments:
        grocery_list -- A dictionary with categories as keys and lists of grocery items as values.
        filepath -- The file to write the list to.
    """  # noqa
    # Sort each category's grocery items alphabetically before writing
    sorted_groceries = {
        category: sorted([item.title() for item in items])
        for category, items in grocery_list.items()
    }
    df = pd.DataFrame({
        "category": sorted_groceries.keys(),
        "grocery_items": [", ".join(items)
                          for items in sorted_groceries.values()]
    })

    # Save with semicolon separator to match original format
    df.to_csv(filepath, sep=";", index=False)
