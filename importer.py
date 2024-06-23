import os
import sys
import threading
import time
from typing import Tuple, Any

import FreeSimpleGUI as sg
import psutil

from select_files_folder import select_directory
from select_project_folder import select_project_folder
from preprocess import preprocess_file
import settings


def process_source_directory(source_directory: str, project_folder: str, log_window: Any) -> Tuple[int, str]:
    # Prompt the user to select a naming convention
    layout = [
        [sg.Text("Select naming convention:")],
        [sg.Combo(["spr_sprite_name", "ESpriteName", "eSpriteName"], key="-NAMING_CONVENTION-", default_value="spr_sprite_name")],
        
        [sg.Checkbox("Overwrite sprite origin", key="-OVERWRITE_ORIGIN-", tooltip="Select if you want to overwrite the origin for all sprites in the import batch. In the next window you will be prompted to provide an origin x and y position. If left unchecked origin will be 0,0")],
        [sg.Checkbox("Overwrite sprite size", key="-OVERWRITE_SIZE-", tooltip="Select if you want to overwrite the width and height for all sprites in the import batch. In the next window you will be prompted to provide a width and height for all sprites.")],
        # [sg.Checkbox("Auto cut canvas", key="-CANVAS_CUTTING-", tooltip="Automatically cut the images based on the filled space in the canvas, ie: if the first pixel starts at x = 2, y = 3, the empty space surrounding the sprite (x < 2, y < 3) will be removed.")],
        [sg.Button("OK"), sg.Button("Cancel")]
    ]
    window = sg.Window("GM Sprite Importer", layout)
    event, values = window.read()
    window.close()

    if event == sg.WINDOW_CLOSED or event == "Cancel":
        return 501, "Cancelled"
        
    settings.naming_convention = values["-NAMING_CONVENTION-"]
    
    # settings.canvas_cutting = values["-CANVAS_CUTTING-"]
    settings.toggle_overwrite_origin = values["-OVERWRITE_ORIGIN-"]
    settings.toggle_overwrite_size = values["-OVERWRITE_SIZE-"]

    if settings.toggle_overwrite_origin:
        sprite_overwrite_origin_layout = [
            [sg.Text("Origin X: "), sg.InputText(key="-X_ORIGIN-", tooltip = "Leave empty if you want to select a relative origin.")],
            [sg.Text("Origin Y: "), sg.InputText(key="-Y_ORIGIN-", tooltip = "Leave empty if you want to select a relative origin.")],
            [sg.Text("Or select a relative origin:", tooltip="Overwrites Origin X and Origin Y, use this to set a relative origin, for top left, use origin x and origin y 0,0 instead.")],
            [sg.Combo(["Disabled", "Top Centre", "Top Right", "Middle Centre", "Bottom Right"], key="-RELATIVE_ORIGIN-", default_value="Disabled")],
            [sg.Button("OK"), sg.Button("Cancel")]
        ]

        sprite_overwrite_origin_window = sg.Window("GM Sprite Importer", sprite_overwrite_origin_layout)
        event, values = sprite_overwrite_origin_window.read()
        sprite_overwrite_origin_window.close()

        settings.x_origin = values["-X_ORIGIN-"]
        settings.y_origin = values["-Y_ORIGIN-"]
        
        # If relative origin is defined and not disabled, we need to use the relative origin instead of x and y origin
        settings.relative_origin = values["-RELATIVE_ORIGIN-"]

        print("Selected relative origin: " + str(settings.relative_origin))


        if event == sg.WINDOW_CLOSED or event == "Cancel":
            settings.toggle_overwrite_origin = False
            settings.x_origin = 0
            settings.y_origin = 0

    if settings.toggle_overwrite_size:
        sprite_overwrite_size_layout = [
            [sg.Text("Sprite width: "), sg.InputText(key="-SPRITE_WIDTH-")],
            [sg.Text("Sprite height: "), sg.InputText(key="-SPRITE_HEIGHT-")],
            [sg.Button("OK"), sg.Button("Cancel")]
        ]
        sprite_overwrite_size_window = sg.Window("GM Sprite Importer", sprite_overwrite_size_layout)
        event, values = sprite_overwrite_size_window.read()
        sprite_overwrite_size_window.close()

        settings.sprite_width = values["-SPRITE_WIDTH-"]
        settings.sprite_height = values["-SPRITE_HEIGHT-"]

        print("x origin: " + str(settings.x_origin))
        print("y origin: " + str(settings.y_origin))
        print("toggle overwrite: " + str(settings.toggle_overwrite_size))
        print("sprite width: " + str(settings.sprite_width))
        print("sprite height: " + str(settings.sprite_height))

        if event == sg.WINDOW_CLOSED or event == "Cancel":
            settings.toggle_overwrite_size = False
            settings.sprite_width = None
            settings.sprite_height = None
            return 200, "Success - Aborted advanced settings."
    
    return 200, "Success"

def log_window_thread(work_id, log_window):
    while True:
        event, values = log_window.read(timeout=1)
        if event == sg.WINDOW_CLOSED:
            current_system_pid = os.getpid()
            this_system = psutil.Process(current_system_pid)
            this_system.terminate()
            time.sleep(5)
        break
        
def main():
    # Log window
    work_id = 0
    log_layout = [
        [sg.Text("Console Output:")],
        [sg.Multiline(size=(80, 20), key="-LOG-", autoscroll=True, reroute_cprint=True)]
    ]
    log_window = sg.Window("GM Sprite Importer Console", log_layout, finalize=True)
    log_thread = threading.Thread(target=log_window_thread, args=(work_id, log_window))
    log_thread.daemon = True
    log_thread.start()

    # Open source directory window
    source_directory = select_directory()

    if source_directory:
        sg.cprint("Source Directory:", source_directory)

        project_folder = select_project_folder(title="Select GameMaker Project Folder")
        is_valid_project_folder = False

        if project_folder:
            # Check if the selected directory contains a yyp file, otherwise cancel:
            files_in_directory = os.listdir(project_folder)
        
            # Check if any file has the .yyp extension
            yyp_file = [file for file in files_in_directory if file.endswith('.yyp')]
            
            if yyp_file and len(yyp_file) == 1:
                sg.cprint(" .yyp file found in the selected project folder.")
                settings.yyp_file = yyp_file[0]
                is_valid_project_folder = True


            if is_valid_project_folder:
                status, message = process_source_directory(source_directory, project_folder, log_window)
            else:
                status, message = 502, "No valid GameMaker project was selected. Make sure the selected folder contains your .yyp file."
                event, values = log_window.read(timeout=0.1)
                if event == sg.WINDOW_CLOSED:
                    pass

            if status == 200:
                sg.cprint("GameMaker Project Folder:", project_folder)
                # Process each file in the source directory
                for root, _, files in os.walk(source_directory):
                    for file in files:
                        source_file = os.path.join(root, file)
                        preprocess_file(source_file, project_folder, settings.naming_convention, log_window)
                        sg.cprint(f"Processed: {source_file}")
                        event, values = log_window.read(timeout=0.1)
                        if event == sg.WINDOW_CLOSED:
                            break
                sg.cprint("Files imported successfully!")
            else:
                sg.cprint(f"File import failed: {str(status)} - {message}")
        else:
            sg.cprint("No valid project folder has been selected.")
    else:
       sg.cprint("No source directory selected.")


    # Event loop for both windows
    while True:
        event, values = log_window.read(timeout=1)  # Timeout to allow both windows to update
        if event == sg.WINDOW_CLOSED:
            break

if __name__ == "__main__":
    main()

    