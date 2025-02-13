from functions.functions import get_todos, write_todos, print_todos

todos = get_todos()

while True:
    user_prompt = "Add [task], Show, Edit [number], Complete [number] or Exit?"
    print(user_prompt)
    user_action = input("- ").strip().capitalize()

    if user_action.startswith('Add'):
        todo = user_action[4:].strip().capitalize()
        todos.append(todo + '\n')
        print(f"{todo} added.")

    elif user_action.startswith('Show'):
        print_todos(todos)

    elif user_action.startswith('Edit'):
        try:
            number = int(user_action[5:])
            print("Enter the new todo for number", number)
            new = input("- ").strip().capitalize()
            todos[number - 1] = new + '\n'
            print_todos(todos)
        except ValueError:
            print("Invalid command. Please type Edit [number].")
            continue

    elif user_action.startswith('Complete'):
        try:
            number = int(user_action[9:])
            complete = todos.pop(number - 1).strip('\n')
            print(f"{complete} completed!")
            print("")
            print_todos(todos)
        except ValueError:
            print("Invalid command. Please type Complete [number].")
            continue
        except IndexError:
            print(
                "There is no item with that number, please enter the correct "
                "number to complete.")
            continue

    elif user_action.startswith('Exit'):
        write_todos(todos)
        break

    else:
        print("Incorrect command, please enter add [task], show, "
              "edit [number], complete [number] or exit.")
        continue

print_todos(todos)
print("")
print("Thank you for using myTodoListApp!")
