# file: nodes/built_in/filters/canny_edge.py

import cv2
import numpy as np
from nodes.base_node import BaseNode
from typing import Dict

ImageType = np.ndarray

class CannyNode(BaseNode):
    """Applies the Canny edge detection algorithm to an image."""
    category = "Filters"
    description = "Detects edges in an image using the Canny algorithm."

    def __init__(self):
        # Define parameters and their default values
        params = {
            "threshold1": 100,
            "threshold2": 200
        }
        super().__init__(
            name="Canny Edge", 
            inputs=["image"], 
            outputs=["image"],
            parameters=params
        )

    def execute(self, **kwargs) -> Dict[str, ImageType]:
        input_image = kwargs.get("image")
        if input_image is None:
            print("  > CannyNode: No input image.")
            return {"image": None}

        # Retrieve the current parameter values from the UI
        t1 = self.param_values["threshold1"]
        t2 = self.param_values["threshold2"]
        
        print(f"  > Applying Canny edge detection with thresholds: {t1}, {t2}")

        # --- Image Processing Logic ---
        # Canny edge detection requires a single-channel (grayscale) image
        if len(input_image.shape) == 3:
            # Convert to grayscale if it's a color image
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        result_image = cv2.Canny(input_image, t1, t2) 
        
        return {"image": result_image}