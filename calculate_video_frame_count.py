import math

class CalculateVideoFrameCount:
    """
    Calculates the total number of video frames required to match a given duration at a specified FPS.
    """

    @classmethod
    def INPUT_TYPES(cls):
        # We use FLOAT for both inputs as duration is always a float,
        # and FPS can be float (e.g., 23.976, 29.97).
        FLOAT_TYPE = ("FLOAT",)

        return {
            "required": {
                "duration": (FLOAT_TYPE, {"default": 1.0, "min": 0.0, "step": 0.01, "display_name": "Duration (s)"}),
                "fps": (FLOAT_TYPE, {"default": 24.0, "min": 1.0, "step": 0.01, "display_name": "Video FPS"}),
            }
        }

    CATEGORY = "🎨 ThimPatUtils/Video Tools"
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("frame_count",)
    FUNCTION = "calculate"
    NODE_DESCRIPTION = "Calculates video frame count from duration and FPS."

    def calculate(self, duration, fps):
        # The core calculation: duration * fps, rounded and cast to INT
        frame_count = int(round(duration * fps))

        # Optional: Print to console for clarity/debugging
        print(f"CalculateVideoFrameCount: {duration}s @ {fps} FPS = {frame_count} frames")

        return (frame_count,)