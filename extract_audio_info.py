import soundfile as sf
import numpy as np
import os  # Import os for path checking (optional, but good practice)


class ExtractAudioInfo:
    @classmethod
    def INPUT_TYPES(cls):
        # NOTE: This uses the revised definition without 'fps' input
        return {
            "required": {
                "audio": ("AUDIO",),
            }
        }

    CATEGORY = "🎨 ThimPatUtils/Audio Tools"

    RETURN_TYPES = ("FLOAT", "INT", "INT", "DICT")
    RETURN_NAMES = (
        "duration",
        "sample_rate",
        "channels",
        "metadata",
    )
    FUNCTION = "extract_audio_info"
    NODE_PATH = "ThimPatUtils/Audio Tools/Extract Audio Info"
    NODE_DESCRIPTION = (
        "Inputs an audio dict or file path, and outputs:\n"
        "- duration (s)\n"
        "- sample_rate (Hz)\n"
        "- channel count\n"
        "- metadata dict\n"
    )

    def extract_audio_info(self, audio):
        print(f"ExtractAudioInfo RECEIVED INPUT DICT: {audio.keys()}")
        
        # pick up aliases
        data_key = next((k for k in audio.keys()
                         if k in ("data", "samples", "array", "waveform")), None)
        sr_key = next((k for k in audio.keys()
                       if k in ("sample_rate", "samplerate", "sr")), None)
        path_key = next((k for k in audio.keys()
                         if k in ("path", "filepath", "filename")), None)

        duration = None  # Initialize duration outside the conditional blocks

        # 1. PRIORITIZE FILE PATH LOADING (Fixes the single-sample bug)
        if path_key:
            path = audio[path_key]

            # --- DEBUG INFO ---
            print(f"ExtractAudioInfo DEBUG: Path found. Prioritizing path loading from: {path}")
            # ------------------

            try:
                # Use soundfile.info to get metadata for the entire file
                info_full = sf.info(path)
                frames = info_full.frames
                sr = info_full.samplerate
                duration = frames / float(sr)
                channels = info_full.channels
                info = {
                    "source": f"sf.info via {path_key}",
                    "format": info_full.format,
                    "subtype": info_full.subtype
                }

                # --- SUCCESS DEBUG ---
                print(f"ExtractAudioInfo DEBUG: File loaded. Frames: {frames}, Duration: {duration:.4f}s")
                # ---------------------

            except Exception as e:
                print(
                    f"ExtractAudioInfo WARNING: Failed to load file from path '{path}': {e}. Falling back to in-memory buffer if available.")

        # 2. FALLBACK TO IN-MEMORY BUFFER (Only if duration wasn't set or path failed)
        if duration is None and data_key and sr_key:
            buffer = audio[data_key]
            sr = int(audio[sr_key])
            frames = buffer.shape[0]
            duration = frames / float(sr)
            channels = audio.get(
                "channels",
                buffer.shape[1] if buffer.ndim > 1 else 1
            )
            info = {
                "source": f"in-memory ({data_key}/{sr_key})",
                "dtype": str(buffer.dtype),
                "frames": frames
            }
            # --- DEBUG INFO ---
            print(f"ExtractAudioInfo DEBUG: Falling back to IN-MEMORY buffer.")
            print(f"ExtractAudioInfo DEBUG: Frames found: {frames}, Sample Rate: {sr}, Duration: {duration}")
            # ------------------

        # 3. ERROR if neither method worked
        if duration is None:
            raise ValueError(
                "ExtractAudioInfo: Failed to get audio information. Need a valid path or an in-memory buffer+sr."
            )

        return (duration, sr, channels, info)