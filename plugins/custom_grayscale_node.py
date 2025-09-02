import cv2
import numpy as np
from nodes.base_node import BaseNode
from typing import Dict

ImageType = np.ndarray


class GrayscaleNode(BaseNode):
    """A custom node that converts a color image to grayscale."""

    category = "Plugins"
    description = "Converts a color image to grayscale."

    def __init__(self):
        super().__init__(name="Grayscale", inputs=["image"], outputs=["image"])

    def execute(self, **kwargs) -> Dict[str, ImageType]:
        input_image = kwargs.get("image")
        if input_image is None:
            return {"image": None}

        if len(input_image.shape) == 3:
            # Convert to grayscale if it's a color image
            result_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        else:
            # If it's already grayscale, just pass it through
            result_image = input_image

        return {"image": result_image}
