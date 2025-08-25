class ExtractImagesFromLatentSync:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "data": ("LATENT",),
            }
        }


    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "convert"

    CATEGORY = "PatUtils"

    def convert(self, data, video_path):
        # Your latent-to-image logic here
        images = data["samples"]  # or however you extract it
        return (images,)


