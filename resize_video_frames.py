import cv2
import numpy as np
import torch

class ResizeVideoFrames:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frame":        ("IMAGE",),
                "target_width": ("INT",   {"default": 512, "min": 64,  "max": 4096}),
                "target_height":("INT",   {"default": 512, "min": 64,  "max": 4096}),
                "mode":         (["stretch", "crop"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION     = "resize"
    CATEGORY     = "ThimPatUtils"

    def resize(self, frame, target_width, target_height, mode):
        # 1) Unpack ComfyUI’s tensor/PIL into a NumPy array
        raw = getattr(frame, "image", frame)
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
            img = nhwc[i]   # H0×W0×C

            # 3) Convert floats→uint8 for OpenCV
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

            # 5) Resize
            if mode == "stretch":
                proc = cv2.resize(cv_in,
                                  (target_width, target_height),
                                  interpolation=cv2.INTER_AREA)
            else:
                aspect = target_width / target_height
                h, w = cv_in.shape[:2]
                if w/h > aspect:
                    nw = int(h * aspect)
                    x0 = (w - nw)//2
                    crop = cv_in[:, x0:x0+nw]
                else:
                    nh = int(w / aspect)
                    y0 = (h - nh)//2
                    crop = cv_in[y0:y0+nh, :]
                proc = cv2.resize(crop,
                                  (target_width, target_height),
                                  interpolation=cv2.INTER_AREA)

            # 6) Swap back to RGB(A)
            if C == 4:
                rgb_u8 = proc[..., [2,1,0,3]]
            elif C == 3:
                rgb_u8 = proc[..., ::-1]
            else:
                rgb_u8 = proc

            # 7) Turn into float32 [0,1]
            # ComfyUI's IMAGE type is (B, H, W, C) in [0,1] float32
            tensor = torch.from_numpy(rgb_u8.astype(np.float32)/255.0) # (H, W, C) float32 in [0,1]
            out_tensors.append(tensor)

        # Combine all HWC tensors into a single BHWC tensor
        # Note: The input conversion logic in your original code results in HWC tensors, 
        # so we stack them directly to create BHWC.
        output_tensor = torch.stack(out_tensors, dim=0) # (B, H, W, C)

        # Return a tuple containing the single BHWC tensor
        return (output_tensor,) 