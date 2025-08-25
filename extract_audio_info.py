# custom_nodes/PatUtils/extract_audio_info.py

import soundfile as sf
import numpy as np

class ExtractAudioInfo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "fps":   ("FLOAT",),   # frames-per-second for video
            }
        }

    RETURN_TYPES = ("FLOAT","INT","INT","DICT","INT")
    RETURN_NAMES = (
        "duration",
        "sample_rate",
        "channels",
        "metadata",
        "frame_count"
    )
    FUNCTION   = "extract_audio_info"
    NODE_PATH  = "PatUtils/Audio Tools/Extract Audio Info"
    NODE_DESCRIPTION = (
        "Inputs an audio dict or file path plus FPS, and outputs:\n"
        "- duration (s)\n"
        "- sample_rate (Hz)\n"
        "- channel count\n"
        "- metadata dict\n"
        "- video frame_count"
    )

    def extract_audio_info(self, audio, fps):
        # pick up aliases
        data_key = next((k for k in audio.keys()
                        if k in ("data","samples","array","waveform")), None)
        sr_key   = next((k for k in audio.keys()
                        if k in ("sample_rate","samplerate","sr")), None)
        path_key = next((k for k in audio.keys()
                        if k in ("path","filepath","filename")), None)

        if data_key and sr_key:
            buffer   = audio[data_key]
            sr       = int(audio[sr_key])
            frames   = buffer.shape[0]
            duration = frames / float(sr)
            channels = audio.get(
                "channels",
                buffer.shape[1] if buffer.ndim > 1 else 1
            )
            info = {
                "source": f"in-memory ({data_key}/{sr_key})",
                "dtype":  str(buffer.dtype),
                "frames": frames
            }

        elif path_key:
            path     = audio[path_key]
            info_full= sf.info(path)
            frames   = info_full.frames
            sr       = info_full.samplerate
            duration = frames / float(sr)
            channels = info_full.channels
            info     = {
                "source":  f"sf.info via {path_key}",
                "format":  info_full.format,
                "subtype": info_full.subtype
            }

        else:
            raise ValueError(
                "ExtractAudioInfo: need an in-memory buffer+sr or a file path."
            )

        frame_count = int(round(duration * fps))
        return (duration, sr, channels, info, frame_count)