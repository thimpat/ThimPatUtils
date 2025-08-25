# 🎥 ComfyUI Multimedia Utilities

A collection of essential utility nodes for handling video, audio, and synchronized data within ComfyUI workflows.

## 🌟 Nodes Included

| Node Display Name | Class Name | Description | Category |
| :--- | :--- | :--- | :--- |
| **🧩 Extract Images from LatentSync** | `ExtractImagesFromLatentSync` | Synchronously extracts and saves a sequence of images from a latent space sequence (often used for video processing) | `video/extract` |
| **🎵 Extract Audio Info** | `ExtractAudioInfo` | Reads an audio file and outputs key information such as sample rate, duration, and number of channels. | `audio/info` |
| **📐 Resize Video Frames** | `ResizeVideoFrames` | Resizes the individual frames of a video sequence (image list) to a specified width and height. | `video/transform` |

## ⬇️ Installation

### Method 1: Using ComfyUI Manager (Recommended)

1.  Open the **ComfyUI Manager**.
2.  Click **"Install Custom Nodes"**.
3.  Search for `Multimedia Utilities` (or your chosen repository name).
4.  Click **"Install"**.
5.  **Restart ComfyUI** to load the new nodes.

### Method 2: Manual Installation (Git Clone)

1.  Navigate to your ComfyUI installation's `custom_nodes` directory:
    ```bash
    cd path/to/ComfyUI/custom_nodes
    ```
2.  Clone this repository:
    ```bash
    git clone [https://github.com/YourGitHubUsername/YourRepoName.git](https://github.com/YourGitHubUsername/YourRepoName.git)
    # ⚠️ Replace the URL with your actual repository URL!
    ```
3.  Install the required Python dependencies (required for video/audio processing):
    ```bash
    # Check the node's specific dependencies and install them into your ComfyUI environment.
    # Example (using embedded Python):
    # path/to/ComfyUI/python_embedded/python.exe -m pip install -r YourRepoName/requirements.txt
    ```
4.  **Restart ComfyUI**.

## ⚙️ Usage & Node Details

### 1. 🧩 Extract Images from LatentSync

This node is ideal when working with models that generate sequences of latents (like latent video models). It ensures the decoded images are processed and saved in the correct sequence and synchronization.

* **Input:** `LATENT` (Sequence of latents), `filename_prefix`, `save_output`
* **Output:** `IMAGE` (Sequence of decoded images)

### 2. 🎵 Extract Audio Info

Use this node to quickly inspect the metadata of an audio file before integrating it into a video or generation workflow.

* **Input:** `audio_path` (string, file path to the audio file)
* **Output:** `duration` (float), `sample_rate` (int), `channels` (int)

### 3. 📐 Resize Video Frames

If your video input or output sequence is the wrong resolution for a subsequent node (e.g., a VAE or a specific model), use this node to quickly scale the frame size.

* **Input:** `IMAGE` (Video/Image sequence), `width` (int), `height` (int), `interpolation` (string, e.g., 'bicubic', 'nearest')
* **Output:** `IMAGE` (Resized video/image sequence)

## 🤝 Contribution

If you have suggestions for new utilities or find a bug, please feel free to open an issue or submit a **Pull Request**.