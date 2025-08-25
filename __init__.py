from .extract_audio_info import ExtractAudioInfo
from .resize_video_frames import ResizeVideoFrames
from .calculate_and_display import CalculateAndDisplay
from .int_float_converter import IntToFloatConverter
from .calculate_video_frame_count import CalculateVideoFrameCount
from .load_path_to_audio_info import LoadPathToAudioInfo

NODE_CLASS_MAPPINGS = {
    "ExtractAudioInfo": ExtractAudioInfo,
    "ResizeVideoFrames": ResizeVideoFrames,
    "CalculateAndDisplay": CalculateAndDisplay,
    "IntToFloatConverter": IntToFloatConverter,
    "CalculateVideoFrameCount": CalculateVideoFrameCount,
    "LoadPathToAudioInfo": LoadPathToAudioInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExtractAudioInfo": "🎵 Extract Audio Info",
    "ResizeVideoFrames": "📐 Resize Video Frames",
    "CalculateAndDisplay": "🔍 Calculate & Display",
    "IntToFloatConverter": "🔢 Int To Float Converter",
    "CalculateVideoFrameCount": "⏱️ Calculate Video Frame Count",
    "LoadPathToAudioInfo": "Load Audio FilePath to Audio Info",
}