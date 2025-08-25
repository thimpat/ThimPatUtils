import torch
import math

class IntToFloatConverter:
    """
    Converts an integer input to a float output.
    Useful for connecting INT outputs (like frame_count) to nodes
    that only accept FLOAT inputs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # This input MUST be INT to connect to the frame_count
                "int_value": ("INT", {"default": 0, "min": 0}),
            }
        }

    CATEGORY = "🎨 ThimPatUtils/Type Converters"
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float_value",)
    FUNCTION = "int_to_float"
    NODE_DESCRIPTION = "Converts an integer (INT) to a floating-point number (FLOAT)."

    def int_to_float(self, int_value):
        # Python's built-in float() function handles the conversion
        float_value = float(int_value)
        return (float_value,)

NODE_CLASS_MAPPINGS = {
    "IntToFloatConverter": IntToFloatConverter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IntToFloatConverter": "🔢 Convert INT to FLOAT",
}