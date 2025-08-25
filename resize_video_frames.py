# resize_video_frames.py

import cv2
import numpy as np

class ResizeVideoFrames:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),  # List of decoded video frames
                "target_width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "target_height": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "mode": (["stretch", "crop"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "resize"

    CATEGORY = "PatUtils"

    def resize(self, frames, target_width, target_height, mode):
        resized = []
        for frame in frames:
            h, w = frame.shape[:2]

            if mode == "stretch":
                resized_frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)

            elif mode == "crop":
                # Center crop before resizing
                aspect_ratio = target_width / target_height
                if w / h > aspect_ratio:
                    new_w = int(h * aspect_ratio)
                    offset = (w - new_w) // 2
                    cropped = frame[:, offset:offset + new_w]
                else:
                    new_h = int(w / aspect_ratio)
                    offset = (h - new_h) // 2
                    cropped = frame[offset:offset + new_h, :]
                resized_frame = cv2.resize(cropped, (target_width, target_height), interpolation=cv2.INTER_AREA)

            resized.append(resized_frame)

        return (resized,)