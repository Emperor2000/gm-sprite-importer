import os
import shutil
import json
from typing import Tuple
import uuid
import imagesize
import settings

import FreeSimpleGUI as sg
from PIL import Image, ImageSequence

from utils import calc_relative_origin

def update_yyp_file(target_folder, prefixed_file_name, project_folder):
    yyp_file_path = os.path.join(project_folder, settings.yyp_file)
    resource_line_index = -1

    with open(yyp_file_path, "r") as f:
        lines = f.readlines()

        # Find the line index containing '"resources":['
        for i, line in enumerate(lines):
            if '"resources":[' in line:
                resource_line_index = i
                break

    if resource_line_index != -1:
        # Add the new resource line
        new_resource = f'    {{"id": {{"name": "{prefixed_file_name}", "path": "sprites/{prefixed_file_name}/{prefixed_file_name}.yy"}},}},\n'
        lines.insert(resource_line_index + 1, new_resource)

        # Write the updated lines back to the .yyp file
        with open(yyp_file_path, "w") as f:
            f.writelines(lines)
    else:
        sg.cprint("Error: 'resources' line not found in the .yyp file.")

def preprocess_file(source_file, target_folder, naming_convention, log_window):
    file_name = os.path.basename(source_file)
    file_extension = os.path.splitext(file_name)[1]

    # Dictionary mapping file extensions to destination folders
    file_types = {
        ".png": "sprites",
        ".gif": "sprites"
        # Add more file types and their destination folders here
    }

    # Get the destination folder based on the file extension
    destination_folder_name = file_types.get(file_extension.lower(), "other")
    destination_folder = os.path.join(target_folder, destination_folder_name)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Apply naming convention prefix
    naming_conventions = {
        "spr_sprite_name": lambda x: x.replace(" ", "_").lower(),
        "eSpriteName": lambda x: ''.join(word.capitalize() for word in x.split()).replace(" ", ""),
        "ESpriteName": lambda x: ''.join(word.capitalize() for word in x.split()).replace(" ", ""),
    }

    # Get the naming convention function based on user selection
    naming_function = naming_conventions.get(naming_convention)

    # Logic for generating the prefix based on the file name and type for snake case convention
    base_file_name = os.path.splitext(file_name)[0]
    prefix = ""
    if naming_convention == "spr_sprite_name":
        if destination_folder_name == "sprites":
            parts = base_file_name.split()
            if len(parts) > 1:
                prefix = "spr_" + "_".join(parts).lower()
            else:
                prefix = "spr_"
        elif destination_folder_name == "objects":
            prefix = "obj_"
        elif destination_folder_name == "audio":
            prefix = "audio_"
        elif destination_folder_name == "notes":
            prefix = "note_"
        elif destination_folder_name == "scripts":
            prefix = "func_"
    if naming_convention == "eSpriteName":
        if destination_folder_name == "sprites":
            prefix = "s"
        elif destination_folder_name == "objects":
            prefix = "o"
        elif destination_folder_name == "audio":
            prefix = "a"
        elif destination_folder_name == "notes":
            prefix = "n"
        elif destination_folder_name == "scripts":
            prefix = "f"
    if naming_convention == "ESpriteName":
        if destination_folder_name == "sprites":
            prefix = "S"
        elif destination_folder_name == "objects":
            prefix = "O"
        elif destination_folder_name == "audio":
            prefix = "A"
        elif destination_folder_name == "notes":
            prefix = "N"
        elif destination_folder_name == "scripts":
            prefix = "F"



        # Generate the destination file name with the prefix
    prefixed_file_name = prefix + naming_function(os.path.splitext(file_name)[0])

    # else:
        # For other naming conventions, use the original file name
        # prefixed_file_name = naming_function(os.path.splitext(file_name)[0])

    # Copy the file to the destination folder with the prefixed name
    destination_file = os.path.join(destination_folder, prefixed_file_name + file_extension)
    # shutil.copy2(source_file, destination_file)

    # If destination folder is "sprites", generate sprite-related files
    if destination_folder_name == "sprites":
        if source_file.lower().endswith('.gif'):
            sprite_sheet, frame_width, frame_height = create_sprite_sheet(source_file)
            settings.current_image_frame_width = frame_width
            settings.current_image_frame_height = frame_height
            #generate_sprite_files(destination_folder, prefixed_file_name, sprite_sheet, naming_convention, project_folder=target_folder)
            return
        generate_sprite_files(destination_folder, prefixed_file_name, source_file, naming_convention, project_folder=target_folder, is_gif=source_file.lower().endswith('.gif'))

def create_sprite_sheet(input_gif_path: str) -> Tuple[str, int, int]:
    # Ensure the input file is a .gif
    if not input_gif_path.lower().endswith('.gif'):
        raise ValueError("Input file must be a .gif")

    # Open the input gif file
    with Image.open(input_gif_path) as im:
        frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
        
        # Get dimensions of each frame
        frame_width, frame_height = frames[0].size

        # Calculate dimensions of the sprite sheet
        sheet_width = frame_width * len(frames)
        sheet_height = frame_height

        # Create a new image for the sprite sheet
        sprite_sheet = Image.new('RGBA', (sheet_width, sheet_height))

        # Paste each frame into the sprite sheet
        for i, frame in enumerate(frames):
            sprite_sheet.paste(frame, (i * frame_width, 0))

        # Save the sprite sheet with the original filename (now as a png file)
        sprite_sheet_path = os.path.splitext(input_gif_path)[0] + '_spritesheet.png'
        sprite_sheet.save(sprite_sheet_path, format='PNG')
        return sprite_sheet_path, frame_width, frame_height

def generate_sprite_files(destination_folder: str, prefixed_file_name: str, source_file: str, naming_convention: str, project_folder: str, is_gif: bool) -> None:
    sg.cprint('generating sprite files for sprite: ' + prefixed_file_name)
    # Generate a unique ID for the sprite frame
    sprite_frame_id = str(uuid.uuid4())

    # Create the sprite folder
    sprite_folder = os.path.join(destination_folder, prefixed_file_name)

    try: 
        os.makedirs(sprite_folder)
    except FileExistsError:
            sg.cprint(f"Folder for sprite: {sprite_folder} already exists.")
    # Copy the image file to the sprites folder
    image_file_path = os.path.join(sprite_folder, f"{sprite_frame_id}.png")
    shutil.copy2(source_file, image_file_path)

    # Create the layers folder
    layers_folder = os.path.join(sprite_folder, "layers")
    layers_subfolder = os.path.join(layers_folder, sprite_frame_id)
    try:
        os.makedirs(layers_folder)
    except FileExistsError:
            sg.cprint(f"Folder {layers_folder} already exists.")
    try:
        os.makedirs(layers_subfolder)
    except FileExistsError:
            sg.cprint(f"Folder {layers_subfolder} already exists.")
    # Creating a sample layer (you may adjust this according to your requirements)
    layer_image_path = os.path.join(layers_folder, f"{layers_subfolder}\\{sprite_frame_id}.png")
    try:
        shutil.copy2(source_file, layer_image_path)
        sg.cprint(f"Successful")
    except FileExistsError:
        sg.cprint(f"File {layer_image_path} already exists")
    # Create the sprite .yy file
    width, height = imagesize.get(layer_image_path)

    if settings.toggle_overwrite_size:
        width = settings.sprite_width
        height = settings.sprite_height

    if settings.relative_origin:
        if is_gif:
            settings.x_origin, settings.y_origin = calc_relative_origin(settings.current_image_frame_width, settings.current_image_frame_height, settings.relative_origin)
        else:
            settings.x_origin, settings.y_origin = calc_relative_origin(width, height, settings.relative_origin)

    sprite_yy_data = {
        "$GMSprite": "",
        "%Name": prefixed_file_name,
        "bboxMode": 0,
        "bbox_bottom": 0,
        "bbox_left": 0,
        "bbox_right": 0,
        "bbox_top": 0,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": [
            {
                "$GMSpriteFrame": "",
                "%Name": sprite_frame_id,
                "name": sprite_frame_id,
                "resourceType": "GMSpriteFrame",
                "resourceVersion": "2.0",
            }
        ],
        "gridX": 0,
        "gridY": 0,
        "height": height,
        "HTile": False,
        "layers": [
            {
                "$GMImageLayer": "",
                "%Name": sprite_frame_id,
                "blendMode": 0,
                "displayName": "Layer 1",
                "isLocked": False,
                "name": sprite_frame_id,
                "opacity": 100.0,
                "resourceType": "GMImageLayer",
                "resourceVersion": "2.0",
                "visible": True,
            }
        ],
        "name": prefixed_file_name,
        "nineSlice": None,
        "origin": 0,
        "parent": {
            "name": "Sprites",
            "path": "folders/Sprites.yy",
        },
        "preMultiplyAlpha": False,
        "resourceType": "GMSprite",
        "resourceVersion": "2.0",
        "sequence": {
            "$GMSequence": "",
            "%Name": prefixed_file_name,
            "autoRecord": True,
            "backdropHeight": 0,
            "backdropImageOpacity": 0.0,
            "backdropImagePath": "",
            "backdropWidth": 0,
            "backdropXOffset": 0.0,
            "backdropYOffset": 0.0,
            "events": {
                "$KeyframeStore<MessageEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MessageEventKeyframe>",
                "resourceVersion": "2.0",
            },
            "eventStubScript": None,
            "eventToFunction": {},
            "length": 0.0,
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0",
            },
            "name": prefixed_file_name,
            "playback": 1,
            "playbackSpeed": 30.0,
            "playbackSpeedType": 0,
            "resourceType": "GMSequence",
            "resourceVersion": "2.0",
            "showBackdrop": False,
            "showBackdropImage": False,
            "timeUnits": 1,
            "tracks": [
                {
                    "$GMSpriteFramesTrack": "",
                    "builtinName": 0,
                    "events": [],
                    "inheritsTrackColour": True,
                    "interpolation": 1,
                    "isCreationTrack": False,
                    "keyframes": {
                        "$KeyframeStore<SpriteFrameKeyframe>": "",
                        "Keyframes": [
                            {
                                "$Keyframe<SpriteFrameKeyframe>": "",
                                "Channels": {
                                    "0": {
                                        "$SpriteFrameKeyframe": "",
                                        "Id": {
                                            "name": sprite_frame_id,
                                            "path": f"sprites/{prefixed_file_name}/{prefixed_file_name}.yy",
                                        },
                                        "resourceType": "SpriteFrameKeyframe",
                                        "resourceVersion": "2.0",
                                    }
                                },
                                "Disabled": False,
                                "id": str(sprite_frame_id),
                                "IsCreationKey": False,
                                "Key": 0.0,
                                "Length": 1.0,
                                "resourceType": "Keyframe<SpriteFrameKeyframe>",
                                "resourceVersion": "2.0",
                                "Stretch": False,
                            }
                        ],
                        "resourceType": "KeyframeStore<SpriteFrameKeyframe>",
                        "resourceVersion": "2.0",
                    },
                    "modifiers": [],
                    "name": "frames",
                    "resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",
                    "spriteId": None,
                    "trackColour": 0,
                    "tracks": [],
                    "traits": 0,
                }
            ],
            "visibleRange": None,
            "volume": 1.0,
            "xorigin": settings.x_origin,
            "yorigin": settings.y_origin,
        },
        "swatchColours": None,
        "swfPrecision": 0.5,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default",
        },
        "type": 0,
        "VTile": False,
        "width": width,
    }

    sprite_yy_file_path = os.path.join(sprite_folder, f"{prefixed_file_name}.yy")
    with open(sprite_yy_file_path, "w") as f:
        json.dump(sprite_yy_data, f, indent=4)

    # Update yyp file
    update_yyp_file(destination_folder, prefixed_file_name, project_folder)