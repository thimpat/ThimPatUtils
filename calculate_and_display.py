import torch
import numpy as np
import math

class CalculateAndDisplay:
    """
    A utility node that evaluates a mathematical formula using up to five
    numerical inputs and displays the result in the console.
    This is useful for debugging and performing quick calculations within
    a ComfyUI workflow.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines the inputs for the node.
        - 'formula': The mathematical expression to evaluate as a string.
        - 'input1' through 'input5': Up to five numerical inputs.
        - 'title': An optional title for the console output.
        """
        return {
            "required": {
                "formula": ("STRING", {"multiline": False, "default": "input1"}),
                "input1": ("FLOAT", {"default": 0.0}),
                "input2": ("FLOAT", {"default": 0.0}),
                "input3": ("FLOAT", {"default": 0.0}),
                "input4": ("FLOAT", {"default": 0.0}),
                "input5": ("FLOAT", {"default": 0.0}),
            },
            "optional": {
                "title": ("STRING", {"multiline": False, "default": "Calculated Value"}),
            }
        }

    # Added a return type so the node can be connected to other nodes
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "calculate"
    CATEGORY = "🎨 ThimPatUtils"

    def calculate(self, formula, input1, input2, input3, input4, input5, title):
        """
        Calculates the result of the given formula and displays it.
        The function uses a safe evaluation method to prevent malicious code
        from being executed.
        """
        # Dictionary of allowed mathematical functions from the 'math' module
        # This prevents arbitrary code execution
        allowed_functions = {
            'abs': abs, 'round': round, 'int': int, 'float': float,
            'sqrt': math.sqrt, 'pow': math.pow, 'exp': math.exp,
            'log': math.log, 'log10': math.log10, 'sin': math.sin,
            'cos': math.cos, 'tan': math.tan, 'radians': math.radians,
            'degrees': math.degrees, 'pi': math.pi, 'e': math.e,
        }

        # Create a dictionary of local variables for the evaluation, including inputs
        local_vars = {
            'input1': input1,
            'input2': input2,
            'input3': input3,
            'input4': input4,
            'input5': input5,
        }
        
        # Add the allowed math functions to the local variables
        local_vars.update(allowed_functions)
        
        try:
            # Safely evaluate the formula using eval with a restricted global environment
            result = eval(formula, {"__builtins__": {}}, local_vars)
            
            # Print the result to the console
            print(f"\n--- {title} ---")
            print(f"Formula: {formula}")
            print(f"Inputs: input1={input1}, input2={input2}, input3={input3}, input4={input4}, input5={input5}")
            print(f"Result: {result}")
            print("--------------------")

            # The node must now return its input to act as a pass-through
            return (result,)

        except Exception as e:
            # Print an error message if the evaluation fails
            print(f"\n--- Calculation Error: {title} ---")
            print(f"Error evaluating formula '{formula}': {e}")
            print("--------------------")
            
            # Return a default value in case of an error to prevent the workflow from crashing
            return (0.0,)

# A dictionary that provides the class name and display name for ComfyUI
NODE_CLASS_MAPPINGS = {
    "CalculateAndDisplay": CalculateAndDisplay
}

# A dictionary that specifies the nodes' human-readable names
NODE_DISPLAY_NAME_MAPPINGS = {
    "CalculateAndDisplay": "🧮 Calculate & Display (Reusable)"
}
