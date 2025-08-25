import soundfile as sf
import os
import folder_paths  # <-- Import folder_paths


class LoadPathToAudioInfo:
    """
    Extracts audio information (duration, sample rate) directly from a file path string.
    Uses ComfyUI's upload mechanism for file selection.
    """

    @classmethod
    def INPUT_TYPES(cls):
        # 1. Get the list of all audio files in the ComfyUI 'input' folder
        audio_extensions = [".wav", ".mp3", ".flac", ".ogg"]
        input_dir = folder_paths.get_input_directory()

        # Filter files based on common audio extensions
        audio_files = [
            f for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
               and os.path.splitext(f)[1].lower() in audio_extensions
        ]

        return {
            "required": {
                # 2. Use the list of found files as the COMBO box options
                "audio_file_name": (audio_files,),
            }
        }

    RETURN_TYPES = ("FLOAT", "INT", "INT", "DICT")
    RETURN_NAMES = ("duration", "sample_rate", "channels", "metadata")
    FUNCTION = "load_info"
    CATEGORY = "🎨 ThimPatUtils/Audio Tools"

    def load_info(self, audio_file_name):
        # 3. Reconstruct the full path to the file in the 'input' folder
        input_dir = folder_paths.get_input_directory()
        file_path = os.path.join(input_dir, audio_file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found at path: {file_path}")

        # The core logic remains the same: load info from the full path
        info_full = sf.info(file_path)
        frames = info_full.frames
        sr = info_full.samplerate
        duration = frames / float(sr)
        channels = info_full.channels

        info = {
            "source": f"Direct Path Load: {audio_file_name}",
            "format": info_full.format,
            "subtype": info_full.subtype
        }

        print(f"LoadPathToAudioInfo SUCCESS: Loaded {frames} frames. Duration: {duration:.4f}s")

        return (duration, sr, channels, info)

NODE_CLASS_MAPPINGS = {
    "LoadPathToAudioInfo": LoadPathToAudioInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadPathToAudioInfo": "🔢 Load Audio FilePath",
}