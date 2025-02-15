
FILEPATH = "list.txt"


def get_todos(filepath: str = FILEPATH) -> list[str]:
    """Read a text file and return each line as a list of to-do items.

    Keyword Arguments:
        filepath -- The file to read (default: {"list.txt"})

    Returns:
        A list with to-do items
    """
    with open(filepath, 'r') as file_local:
        todos_local = file_local.readlines()
    return todos_local


def write_todos(todo_list: list[str],
                filepath: str = FILEPATH) -> None:
    """Write the items in the todo_list to a file
    Arguments:
        todo_list -- A List of to-do items to write to a file

    Keyword Arguments:
        filepath -- The file to write the list to (default: {"list.txt"})
    """
    todo_list = [item for item in todo_list]
    with open(filepath, 'w') as file_local:
        file_local.writelines(todo_list)


def print_todos(todo_list: list[str]) -> None:
    """"Prints out the current to-do list.

    Arguments:
        todo_list -- The to-do list to print.
    """
    print("Current to-do list:")
    for index, item in enumerate(todo_list):
        row = f"{index +1}. {item.capitalize()}"
        print(row.strip('\n'))
