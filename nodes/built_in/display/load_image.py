
import numpy as np
import cv2
from typing import Dict
from nodes.base_node import BaseNode

ImageType = np.ndarray

class LoadImageNode(BaseNode):
    """Loads an image from a file path."""
    category = "IO"
    description = "Loads an image from a specified file path."

    def __init__(self):
        # Default path is now our sample image
        super().__init__(name="Load Image", inputs=[], outputs=["image"], parameters={"path": "sample_data/checkerboard.png"})

    def execute(self, **kwargs) -> Dict[str, ImageType]:
        path = self.param_values["path"]
        print(f"  > Loading image from: {path}")
        
        # Use OpenCV to load the image
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"  > Error: Could not load image from {path}")
            # Return a black 10x10 image as a fallback
            return {"image": np.zeros((10, 10), dtype=np.uint8)}
            
        return {"image": image}
