# 🎥 ComfyUI Multimedia Utilities

A collection of essential utility nodes for handling image sequences, video, audio, and synchronized data within ComfyUI workflows.

---

## 🌟 Nodes Included

| Node Display Name                      | Class Name                   | Description                                                                                   | Category           |
| :------------------------------------- | :--------------------------- | :-------------------------------------------------------------------------------------------- | :----------------- |
| **🧩 Extract Images from LatentSync**   | `ExtractImagesFromLatentSync` | Synchronously extracts and saves a sequence of images from a latent space sequence.           | `video/extract`    |
| **🎵 Extract Audio Info**               | `ExtractAudioInfo`           | Reads an audio file and outputs key information such as sample rate, duration, and channels.  | `audio/info`       |
| **📐 Resize Image Sequence**            | `ResizeVideoFrames`          | Resizes each image in an input sequence to a specified width and height.                     | `video/transform`  |

---

## ⬇️ Installation

### Method 1: Using ComfyUI Manager (Recommended)

1.  Open the **ComfyUI Manager**.  
2.  Click **Install Custom Nodes**.  
3.  Search for **Multimedia Utilities**.  
4.  Click **Install**.  
5.  **Restart ComfyUI** to load the new nodes.

### Method 2: Manual Installation (Git Clone)

1.  Navigate to your ComfyUI installation’s `custom_nodes` directory:  
    ```bash
    cd path/to/ComfyUI/custom_nodes
    ```
2.  Clone this repository:  
    ```bash
    git clone https://github.com/thimpat/ThimPatUtils.git
    ```
3.  Install the required Python dependencies into your ComfyUI environment:  
    ```bash
    # Example (using embedded Python):
    # path/to/ComfyUI/python_embedded/python.exe -m pip install -r ThimPatUtils/requirements.txt
    ```
4.  **Restart ComfyUI**.

---

## ⚙️ Usage & Node Details

### 1. 🧩 Extract Images from LatentSync

This node takes a sequence of latents (for example, from a latent‐video model) and produces a synchronized list of decoded images.

- **Inputs:**  
  - `LATENT` (Sequence of latents)  
  - `filename_prefix` (string)  
  - `save_output` (boolean)  
- **Outputs:**  
  - `IMAGE` (Sequence of decoded images)  

---

### 2. 🎵 Extract Audio Info

Quickly inspect an audio file’s metadata before feeding it into a generation or editing pipeline.

- **Inputs:**  
  - `audio_path` (string, path to the audio file)  
- **Outputs:**  
  - `duration` (float)  
  - `sample_rate` (int)  
  - `channels` (int)  

---

### 3. 📐 Resize Image Sequence

Rescales each image in an input sequence—ideal when a downstream node (e.g., a VAE or model) requires a specific resolution.

<video src="./demo/demo-resize-frames.mp4" controls muted autoplay loop style="max-width: 100%; height: auto; border-radius: 12px;"></video>

- **Inputs:**  
  - `images` (Image sequence)  
  - `width` (int)  
  - `height` (int)  
  - `interpolation` (string; options: `bicubic`, `nearest`, etc.)  
- **Outputs:**  
  - `IMAGE` (Resized image sequence)  

---

## 🤝 Contribution

If you have ideas for new utilities or spot a bug, please open an issue or submit a Pull Request. We welcome your feedback and improvements!

## Author

Find my other projects on https://perspectivedev.com/gb/market.html#/authors/1