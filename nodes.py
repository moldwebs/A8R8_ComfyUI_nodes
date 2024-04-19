import base64
from PIL import Image
import torch
import numpy as np
import io


class Base64ImageInput:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "bas64_image": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "test"

    CATEGORY = "A8R8"

    def test(self, bas64_image):
        if bas64_image:
            image_bytes = base64.b64decode(bas64_image)

            # Open the image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            return (image,)


class Base64ImageOutput:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                {"images": ("IMAGE", ), },
                }

    RETURN_TYPES = ()

    FUNCTION = "test"

    OUTPUT_NODE = True

    CATEGORY = "A8R8"

    def test(self, images: list[torch.Tensor]):
        image = images[0]
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        buffered = io.BytesIO()
        img.save(buffered, optimize=False,
                 format='png', compress_level=4)

        base64_image = base64.b64encode(buffered.getvalue()).decode()

        return {"ui": {"base64_images": [base64_image]}}


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Base64ImageInput": Base64ImageInput,
    "Base64ImageOutput": Base64ImageOutput
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Base64ImageInput": "Base64Image Input Node",
    "Base64ImageOutput": "Base64Image Output Node"
}
