import torch
import numpy as np
import collections

class PreviewInfo:
    """
    A utility node to preview information about any type of input in the console.
    This node is useful for debugging and checking the values of variables
    at different points in a workflow. It acts as a final node in the workflow,
    stopping the execution chain.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines the inputs for the node. It accepts a single, generic input of
        any type, and an optional title for clarity in the console.
        """
        return {
            "required": {
                "input_data": ("*", {"forceInput": True}),  # The asterisk (*) signifies any data type
            },
            "optional": {
                "title": ("STRING", {"multiline": False, "default": "Preview Any"}),
            }
        }

    # The node now has no return types, making it a "final" or "sink" node.
    RETURN_TYPES = ()
    FUNCTION = "preview_info"
    CATEGORY = "🎨 ThimPatUtils"

    def preview_info(self, input_data, title):
        """
        The main function of the node. It prints the type, value, and other
        relevant information about the input data to the console.
        """
        print(f"\n--- {title} ---")
        
        # Check the type of the input_data
        if isinstance(input_data, torch.Tensor):
            # If the input is a PyTorch tensor (e.g., IMAGE, LATENT)
            print("Type: torch.Tensor (ComfyUI IMAGE/LATENT)")
            print(f"Shape: {input_data.shape}")
            print(f"Data type: {input_data.dtype}")
            print(f"Min value: {input_data.min().item():.4f}")
            print(f"Max value: {input_data.max().item():.4f}")
            if input_data.nelement() <= 20: # Display small tensors fully
                print(f"Value: \n{input_data}")
        
        elif isinstance(input_data, list) and all(isinstance(item, torch.Tensor) for item in input_data):
            # If the input is a list of tensors (e.g., a list of images)
            print("Type: List of torch.Tensor")
            print(f"Number of tensors in list: {len(input_data)}")
            if len(input_data) > 0:
                first_tensor = input_data[0]
                print(f"First tensor shape: {first_tensor.shape}")
                print(f"First tensor data type: {first_tensor.dtype}")
                print(f"First tensor min value: {first_tensor.min().item():.4f}")
                print(f"First tensor max value: {first_tensor.max().item():.4f}")

        elif isinstance(input_data, str):
            # If the input is a string
            print("Type: STRING")
            print(f"Value: \"{input_data}\"")
        
        elif isinstance(input_data, (int, float)):
            # If the input is a number
            print("Type: NUMBER")
            print(f"Value: {input_data}")

        elif isinstance(input_data, dict):
            # If the input is a dictionary (e.g., AUDIO)
            print("Type: DICT")
            print(f"Keys: {list(input_data.keys())}")
            # Optional: print some key-value pairs for common dictionary types
            for key, value in input_data.items():
                print(f"  {key}: {value}")
            
        elif isinstance(input_data, collections.abc.Iterable):
            # If the input is another iterable type (e.g., a list of strings)
            print("Type: Iterable")
            print(f"Value: {input_data}")
            
        else:
            # For any other unsupported or unknown type
            print("Type: UNKNOWN or unsupported")
            print(f"Python Type: {type(input_data)}")
            print(f"Value: {input_data}")

        print("--------------------")

        # No return statement is needed, as this is a final node.

# A dictionary that provides the class name and display name for ComfyUI
NODE_CLASS_MAPPINGS = {
    "PreviewInfo": PreviewInfo
}

# A dictionary that specifies the nodes' human-readable names
NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewInfo": "👁️ Preview Info"
}
