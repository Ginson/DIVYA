from nodes.base_node import BaseNode
from typing import Dict
import numpy as np
from PyQt6.QtCore import pyqtSignal

class DisplayNode(BaseNode):
    """A node that displays an image in the UI."""
    category = "Display"
    description = "Displays an image in the main UI."
    # Define a signal that will carry the image data (as a numpy array)
    image_processed = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__(name="Display Image", inputs=["image"], outputs=[])

    def execute(self, **kwargs) -> Dict:
        image = kwargs.get("image")
        if image is not None:
            print(f"  > DisplayNode: Emitting image with shape: {image.shape}")
            # Emit the signal with the image data
            self.image_processed.emit(image)
        else:
            print("  > DisplayNode: No image to display.")
            # Emit a None value to clear the display
            self.image_processed.emit(np.array([])) 
        return {}
