import cv2
import numpy as np
import torch

class ResizeVideoFrames:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images":       ("IMAGE",),
                "target_width": ("INT",   {"default": 512, "min": 64,  "max": 4096}),
                "target_height":("INT",   {"default": 512, "min": 64,  "max": 4096}),
                # Add 'pad' to the list of modes
                "mode":         (["stretch", "crop", "pad"],),
                "crop_position":(["center", "top", "bottom", "left", "right"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION     = "resize"
    CATEGORY     = "🎨 ThimPatUtils"

    def resize(self, images, target_width, target_height, mode, crop_position):
        # 1) Unpack ComfyUI’s tensor/PIL into a NumPy array
        raw = getattr(images, "image", images)
        if isinstance(raw, torch.Tensor):
            arr = raw.detach().cpu().numpy()
        else:
            arr = np.asarray(raw)

        # 2) Normalize into NHWC batch
        if arr.ndim == 4:
            if arr.shape[-1] <= 4:
                nhwc = arr
            else:
                nhwc = arr.transpose(0, 2, 3, 1)
        elif arr.ndim == 3:
            if arr.shape[0] <= 4:
                nhwc = arr.transpose(1, 2, 0)[None]
            else:
                nhwc = arr[None]
        else:
            raise ValueError(f"ResizeVideoFrames: unsupported dims {arr.shape}")

        B, H0, W0, C = nhwc.shape
        out_tensors = []

        for i in range(B):
            img = nhwc[i]   # H0xW0xC

            # 3) Convert floats->uint8 for OpenCV
            if img.dtype != np.uint8:
                img_u8 = (np.clip(img, 0.0, 1.0) * 255.0).round().astype(np.uint8)
            else:
                img_u8 = img

            # 4) BGR swap
            if C == 4:
                cv_in = img_u8[..., [2,1,0,3]]
            elif C == 3:
                cv_in = img_u8[..., ::-1]
            else:
                cv_in = img_u8

            # 5) Resize and/or Pad
            if mode == "stretch":
                proc = cv2.resize(cv_in,
                                  (target_width, target_height),
                                  interpolation=cv2.INTER_AREA)
            elif mode == "crop":
                # Calculate the crop
                aspect = target_width / target_height
                h, w = cv_in.shape[:2]
                
                x0, y0 = 0, 0
                
                # If the image is wider than the target aspect ratio, crop horizontally
                if w / h > aspect:
                    nw = int(h * aspect)
                    if crop_position == "center":
                        x0 = (w - nw) // 2
                    elif crop_position == "left":
                        x0 = 0
                    elif crop_position == "right":
                        x0 = w - nw
                    crop = cv_in[:, x0:x0 + nw]
                # If the image is taller than the target aspect ratio, crop vertically
                else:
                    nh = int(w / aspect)
                    if crop_position == "center":
                        y0 = (h - nh) // 2
                    elif crop_position == "top":
                        y0 = 0
                    elif crop_position == "bottom":
                        y0 = h - nh
                    crop = cv_in[y0:y0 + nh, :]
                
                # After cropping, resize to the target dimensions
                proc = cv2.resize(crop,
                                  (target_width, target_height),
                                  interpolation=cv2.INTER_AREA)
            elif mode == "pad":
                # Calculate pad dimensions
                h, w = cv_in.shape[:2]
                aspect = target_width / target_height
                
                # Resize the image while maintaining aspect ratio
                if w / h > aspect:
                    # Image is wider, pad vertically
                    new_w = target_width
                    new_h = int(h * (target_width / w))
                    resized_img = cv2.resize(cv_in, (new_w, new_h), interpolation=cv2.INTER_AREA)
                    # Create a black canvas for the final image
                    canvas = np.zeros((target_height, target_width, C), dtype=np.uint8)
                    # Pad
                    y_start = (target_height - new_h) // 2
                    canvas[y_start:y_start + new_h, :, :] = resized_img
                else:
                    # Image is taller, pad horizontally
                    new_h = target_height
                    new_w = int(w * (target_height / h))
                    resized_img = cv2.resize(cv_in, (new_w, new_h), interpolation=cv2.INTER_AREA)
                    # Create a black canvas for the final image
                    canvas = np.zeros((target_height, target_width, C), dtype=np.uint8)
                    # Pad
                    x_start = (target_width - new_w) // 2
                    canvas[:, x_start:x_start + new_w, :] = resized_img

                proc = canvas

            # 6) Swap back to RGB(A)
            if C == 4:
                rgb_u8 = proc[..., [2,1,0,3]]
            elif C == 3:
                rgb_u8 = proc[..., ::-1]
            else:
                rgb_u8 = proc

            # 7) Turn into float32 [0,1]
            tensor = torch.from_numpy(rgb_u8.astype(np.float32) / 255.0)

            # Append the HWC tensor to our list.
            out_tensors.append(tensor)

        # After the loop, stack all HWC tensors into a single BHWC tensor.
        output_tensor = torch.stack(out_tensors, dim=0)

        # Return a tuple containing the single BHWC tensor.
        return (output_tensor,)
