import functions.functions as f
import FreeSimpleGUI as sg
import time

todos = f.get_todos()
todos = [item.strip() for item in todos]

clock = sg.Text('', key="clock")
add_label = sg.Text("Enter a to-do")
add_input_box = sg.InputText(tooltip="Enter a to-do: ", key="todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values=todos,
                      key="todo_list",
                      enable_events=True,
                      size=(25, len(todos)),
                      select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)
edit_button = sg.Button("Edit")
complete_button = sg.Button("Complete")
exit_button = sg.Button("Exit")

content = [[clock],
           [add_label],
           [add_input_box, add_button],
           [list_box, sg.Column([[edit_button], [complete_button]])],
           [exit_button]]

window = sg.Window("To-Do App",
                   layout=[[sg.Column(content)]])


while True:
    event, values = window.read(timeout=1)
    match event:
        case "Add":
            new_todo = values['todo'] + "\n"
            todos.append(new_todo)
            window['todo_list'].update(values=todos)
        case "Edit":
            try:
                todo_to_edit = values['todo_list'][0].strip()
                new_value = sg.popup_get_text(
                    "New to-do item:", title="Edit",
                    default_text=f"{todo_to_edit}")
                edit_index = todos.index(todo_to_edit)
                todos[edit_index] = new_value
                window['todo_list'].update(values=todos)
            except IndexError:
                sg.popup("Please select which task to edit.")
        case "Complete":
            try:
                todo_to_complete = values['todo_list'][0]
                todos.remove(todo_to_complete)
                window['todo_list'].update(values=todos)
            except IndexError:
                sg.popup("Please select which task to complete.")
        case "Exit" | sg.WIN_CLOSED:
            f.write_todos(todos)
            break
    window["clock"].update(value=time.strftime("%a, %d %B %Y - %H:%M:%S"))
window.close
