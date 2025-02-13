import functions.functions as f
import FreeSimpleGUI as fsg

todos = f.get_todos()
todos = [item.strip() for item in todos]

empty_label = fsg.Text()
add_label = fsg.Text("Enter a to-do")
add_input_box = fsg.InputText(tooltip="Enter a to-do: ", key="todo")
add_button = fsg.Button("Add")
list_box = fsg.Listbox(values=todos,
                       key="todo_list",
                       enable_events=True,
                       size=(25, len(todos)),
                       select_mode=fsg.LISTBOX_SELECT_MODE_SINGLE)
edit_button = fsg.Button("Edit")
complete_button = fsg.Button("Complete")
exit_button = fsg.Button("Exit")

content = [[add_label],
           [add_input_box, add_button],
           [list_box, fsg.Column([[edit_button], [complete_button]])],
           [exit_button]]

window = fsg.Window("To-Do App",
                    layout=[[fsg.Column(content)]])


while True:
    event, values = window.read()
    match event:
        case "Add":
            new_todo = values['todo'] + "\n"
            todos.append(new_todo)
            window['todo_list'].update(values=todos)
        case "Edit":
            todo_to_edit = values['todo_list'][0].strip()
            new_value = fsg.popup_get_text(
                "New to-do item:", title="Edit",
                default_text=f"{todo_to_edit}")
            edit_index = todos.index(todo_to_edit)
            todos[edit_index] = new_value
            window['todo_list'].update(values=todos)
        case "Exit" | fsg.WIN_CLOSED:
            f.write_todos(todos)
            break
window.close
