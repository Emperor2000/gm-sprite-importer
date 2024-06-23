import json
import os
import shutil
import uuid

def generate_sprite_files(destination_folder, prefix, source_file):
    # Generate a unique ID for the sprite frame
    sprite_frame_id = str(uuid.uuid4())

    # Create the sprite folder
    sprite_folder = os.path.join(destination_folder, prefix)
    os.makedirs(sprite_folder)

    # Copy the image file to the sprites folder
    image_file_path = os.path.join(sprite_folder, f"{sprite_frame_id}.png")
    shutil.copy2(source_file, image_file_path)

    # Create the layers folder
    layers_folder = os.path.join(sprite_folder, "layers")
    os.makedirs(layers_folder)

    # Creating a sample layer (you may adjust this according to your requirements)
    layer_image_path = os.path.join(layers_folder, f"{sprite_frame_id}.png")
    shutil.copy2(source_file, layer_image_path)

    # Create the sprite .yy file
    sprite_yy_data = {
        "$GMSprite": "",
        "%Name": prefix,
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
        "height": 0,
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
        "name": prefix,
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
            "%Name": prefix,
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
            "name": prefix,
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
                                            "path": f"sprites/{prefix}/{prefix}.yy",
                                        },
                                        "resourceType": "SpriteFrameKeyframe",
                                        "resourceVersion": "2.0",
                                    }
                                },
                                "Disabled": False,
                                "id": str(uuid.uuid4()),
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
            "xorigin": 0,
            "yorigin": 0,
        },
        "swatchColours": None,
        "swfPrecision": 0.5,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default",
        },
        "type": 0,
        "VTile": False,
        "width": 0,
    }

    sprite_yy_file_path = os.path.join(sprite_folder, f"{prefix}.yy")
    with open(sprite_yy_file_path, "w") as f:
        json.dump(sprite_yy_data, f, indent=4)



def preprocess_file(source_file, target_folder, naming_convention):
    file_name = os.path.basename(source_file)
    file_extension = os.path.splitext(file_name)[1]

    # Dictionary mapping file extensions to destination folders
    file_types = {
        ".png": "sprites",
        ".txt": "notes",
        # Add more file types and their destination folders here
    }

    # Get the destination folder based on the file extension
    destination_folder = file_types.get(file_extension.lower(), "other")
    destination_folder = os.path.join(target_folder, destination_folder)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Apply naming convention prefix
    naming_conventions = {
        "typ_snakecase": lambda x: f"{naming_convention}_{x}",
        "tPascalCase": lambda x: f"{naming_convention.capitalize()}{x.capitalize()}",
        "TCamelCase": lambda x: f"{naming_convention}{x.capitalize()}",
    }

    # Get the naming convention function based on user selection
    naming_function = naming_conventions.get(naming_convention)

    # Logic for generating the prefix based on the file name and type for snake case convention
    if naming_convention == "typ_snakecase":
        base_file_name = os.path.splitext(file_name)[0]
        prefix = ""
        if destination_folder == "sprites":
            parts = base_file_name.split()
            if len(parts) > 1:
                prefix = "spr_" + "_".join(parts).lower()
            else:
                prefix = "spr_" + base_file_name.lower()
        elif destination_folder == "objects":
            prefix = "obj_" + base_file_name.lower()
        elif destination_folder == "audio":
            prefix = "audio_" + base_file_name.lower()
        elif destination_folder == "notes":
            prefix = "note_" + base_file_name.lower()
        elif destination_folder == "scripts":
            prefix = "func_" + base_file_name.lower()

        # Generate the destination file name with the prefix
        prefixed_file_name = naming_function(prefix)
    else:
        # For other naming conventions, use the original file name
        prefixed_file_name = naming_function(os.path.splitext(file_name)[0])

    # Copy the file to the destination folder with the prefixed name
    destination_file = os.path.join(destination_folder, prefixed_file_name + file_extension)
    shutil.copy2(source_file, destination_file)