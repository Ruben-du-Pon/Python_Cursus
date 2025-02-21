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


def get_groceries(filepath: str = DEFAULT_GROCERIES) -> dict[str: list]:
    """Read a text file and return each line as a list of grocery items.

    Keyword Arguments:
        filepath -- The file to read (default: {"default_groceries.csv"})

    Returns:
        A list with grocery items
    """
    df = pd.read_csv(filepath, header=None)
    groceries_local = df.to_dict("split")
    return groceries_local


def write_groceries(grocery_list: dict[str: list],
                    filepath: str = DEFAULT_GROCERIES) -> None:
    """Write the items in the grocery_list to a file
    Arguments:
        grocery_list -- A grocery list to write to a file

    Keyword Arguments:
        filepath -- The file to write the list to
                    (default: {"default_groceries.txt"})
    """
    df = pd.DataFrame.from_dict(grocery_list)
    df.to_csv(filepath, index=False)
