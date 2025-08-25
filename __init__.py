from .extract_images_node   import ExtractImagesFromLatentSync
from .extract_audio_info    import ExtractAudioInfo
from .resize_video_frames   import ResizeVideoFrames

NODE_CLASS_MAPPINGS = {
    "ExtractImagesFromLatentSync": ExtractImagesFromLatentSync,
    "ExtractAudioInfo":              ExtractAudioInfo,
    "ResizeVideoFrames":              ResizeVideoFrames
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExtractImagesFromLatentSync": "🧩 Extract Images from LatentSync",
    "ExtractAudioInfo":              "🎵 Extract Audio Info",
    "ResizeVideoFrames":              "📐 Resize Video Frames"
}