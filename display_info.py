import torch
import numpy as np
import collections
import json

class DisplayInfo:
    """
    A utility node to display information about any type of input
    in a textarea within the node itself.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "display_text": ("STRING", {"multiline": True, "default": "No data received yet"}),
            },
            "optional": {
                "input_data": ("*", {"default": None}),
                "trigger": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "display_info"
    CATEGORY = "🎨 ThimPatUtils"
    OUTPUT_NODE = True

    def display_info(self, display_text, input_data=None, trigger=True):
        output = "--- Display Info ---\n"

        try:
            if input_data is None:
                output += "No input data received\n"
            elif isinstance(input_data, torch.Tensor):
                output += "Type: torch.Tensor (ComfyUI IMAGE/LATENT)\n"
                output += f"Shape: {input_data.shape}\n"
                output += f"Data type: {input_data.dtype}\n"
                output += f"Min value: {input_data.min().item():.4f}\n"
                output += f"Max value: {input_data.max().item():.4f}\n"
                if input_data.nelement() <= 20:
                    output += f"Value:\n{input_data}\n"

            elif isinstance(input_data, list) and all(isinstance(t, torch.Tensor) for t in input_data):
                output += "Type: List of torch.Tensor\n"
                output += f"Count: {len(input_data)}\n"
                t0 = input_data[0]
                output += f"First tensor shape: {t0.shape}\n"
                output += f"First tensor dtype: {t0.dtype}\n"
                output += f"First tensor min: {t0.min().item():.4f}\n"
                output += f"First tensor max: {t0.max().item():.4f}\n"

            elif isinstance(input_data, str):
                output += "Type: STRING\n"
                output += f"Value: \"{input_data}\"\n"

            elif isinstance(input_data, (int, float)):
                output += "Type: NUMBER\n"
                output += f"Value: {input_data}\n"

            elif isinstance(input_data, dict):
                output += "Type: DICT\n"
                output += f"Keys: {list(input_data.keys())}\n"
                for k, v in input_data.items():
                    try:
                        vs = json.dumps(v, indent=2, sort_keys=True)
                        output += f"  {k}:\n{vs}\n"
                    except:
                        output += f"  {k}: {v}\n"

            elif isinstance(input_data, collections.abc.Iterable):
                output += "Type: Iterable\n"
                output += f"Value: {input_data}\n"

            else:
                output += "Type: UNKNOWN\n"
                output += f"Python Type: {type(input_data)}\n"
                output += f"Value: {input_data}\n"

        except Exception as e:
            output += f"Error processing input data: {e}\n"
            output += f"Input type was: {type(input_data)}\n"

        output += "--------------------\n"

        # Return the updated text for the textarea
        return {"ui": {"text": output}}


# A dictionary that provides the class name and display name for ComfyUI
NODE_CLASS_MAPPINGS = {
    "DisplayInfo": DisplayInfo
}

# A dictionary that specifies the nodes' human-readable names
NODE_DISPLAY_NAME_MAPPINGS = {
    "DisplayInfo": "👁️ Display Info"
}