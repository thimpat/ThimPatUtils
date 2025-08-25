import torch
import numpy as np
import math


class CalculateAndDisplay:
    """
    A utility node that evaluates a mathematical formula using up to five
    numerical inputs and displays the result in the console AND on the node.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines the inputs for the node.
        - 'formula': The mathematical expression to evaluate as a string.
        - 'input1' through 'input5': Up to five numerical inputs.
        """
        return {
            "required": {
                "formula": ("STRING", {"multiline": False, "default": "input1"}),
                "input1": ("FLOAT", {"default": 0.0}),
                "input2": ("FLOAT", {"default": 0.0}),
                "input3": ("FLOAT", {"default": 0.0}),
                "input4": ("FLOAT", {"default": 0.0}),
                "input5": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("FLOAT", "STRING")
    RETURN_NAMES = ("result", "display_text")
    FUNCTION = "calculate"
    CATEGORY = "🎨 ThimPatUtils"
    OUTPUT_NODE = True

    def calculate(self, formula, input1, input2, input3, input4, input5):
        CONSOLE_TITLE = "CALCULATION RESULT"

        allowed_functions = {
            'abs': abs, 'round': round, 'int': int, 'float': float,
            'sqrt': math.sqrt, 'pow': math.pow, 'exp': math.exp,
            'log': math.log, 'log10': math.log10, 'sin': math.sin,
            'cos': math.cos, 'tan': math.tan, 'radians': math.radians,
            'degrees': math.degrees, 'pi': math.pi, 'e': math.e,
        }

        local_vars = {
            'input1': input1, 'input2': input2, 'input3': input3,
            'input4': input4, 'input5': input5,
        }
        local_vars.update(allowed_functions)

        try:
            result = eval(formula, {"__builtins__": {}}, local_vars)

            print(f"\n--- {CONSOLE_TITLE} ---")
            print(f"Formula: {formula}")
            print(f"Inputs: input1={input1}, input2={input2}, input3={input3}, input4={input4}, input5={input5}")
            print(f"Result: {result}")
            print("--------------------")

            # Create display text for the UI
            display_text = f"Formula: {formula}\nResult: {result}"

            # Return the result, display text, and UI info
            return ((result, display_text), {"ui": {"text": [display_text]}})

        except Exception as e:
            # The except block's logic is already correct
            print(f"\n--- Calculation Error: {CONSOLE_TITLE} ---")
            print(f"Error evaluating formula '{formula}': {e}")
            print("--------------------")

            display_text = f"Error: {e}"
            return ((0.0, display_text), {"ui": {"text": [display_text]}})


# ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "CalculateAndDisplay": CalculateAndDisplay
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CalculateAndDisplay": "🧮 Calculate & Display (Reusable)"
}