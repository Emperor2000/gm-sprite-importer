import FreeSimpleGUI as sg
from typing import Optional

def select_directory() -> Optional[str]:
    layout = [
        [sg.Text("Always back-up your GameMaker project before use!")],
        [sg.Text("Select directory of files to import:")],
        [sg.InputText(key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Button("OK"), sg.Button("Cancel")]
    ]

    window = sg.Window("GM Sprite Importer", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Cancel":
            directory_path = None
            break
        elif event == "OK":
            directory_path = values["-FOLDER-"]
            break

    window.close()

    return directory_path

if __name__ == "__main__":
    directory_path = select_directory()
    
    if directory_path:
        sg.cprint("Selected Directory:", directory_path)
    else:
        sg.cprint("No directory selected.")