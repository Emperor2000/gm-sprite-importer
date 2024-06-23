import FreeSimpleGUI as sg

def select_project_folder(title="Select GameMaker Project Folder"):
    layout = [
        [sg.Text("Select directory of GM project:")],
        [sg.InputText(key="-PROJECT_FOLDER-"), sg.FolderBrowse()],
        [sg.Button("OK"), sg.Button("Cancel")]
    ]

    window = sg.Window(title, layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Cancel":
            project_folder = None
            break
        elif event == "OK":
            project_folder = values["-PROJECT_FOLDER-"]
            break

    window.close()

    return project_folder