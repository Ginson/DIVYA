from nodes.base_node import BaseNode
from typing import Dict
import numpy as np
import cv2

ImageType = np.ndarray


class BlurNode(BaseNode):
    """Blurs an image using a simple box filter."""

    category = "Filters"
    description = "Applies a blur to an image."

    def __init__(self):
        super().__init__(
            name="Blur",
            inputs=["image"],
            outputs=["image"],
            parameters={"kernel_size": 5},
        )

    def execute(self, **kwargs) -> Dict[str, ImageType]:
        image = kwargs.get("image")
        if image is None:
            print("  > BlurNode: No input image.")
            return {"image": None}

        kernel_size = self.param_values["kernel_size"]
        # Kernel size must be an odd number
        if kernel_size % 2 == 0:
            kernel_size += 1

        print(f"  > Applying blur with kernel size: {kernel_size}")

        # Apply the blur using OpenCV
        blurred_image = cv2.blur(image, (kernel_size, kernel_size))

        return {"image": blurred_image}
