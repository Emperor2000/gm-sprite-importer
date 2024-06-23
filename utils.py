from typing import Tuple

def calc_relative_origin(image_width: int, image_height: int, relative_origin: str) -> Tuple[int, int]:
    origin_x = 0
    origin_y = 0

    match relative_origin:
        # case "Disabled":
            # Added for visibility
        case "Top Centre":
            origin_x = image_width/2
            origin_y = 0
        case "Top Right":
            origin_x = image_width
            origin_y = 0
        case "Middle Centre":
            origin_x = image_width/2
            origin_y = image_height/2
        case "Bottom Right":
            origin_x = image_width
            origin_y = image_height

    rounded_origin_x = round(origin_x)
    rounded_origin_y = round(origin_y)

    return rounded_origin_x, rounded_origin_y