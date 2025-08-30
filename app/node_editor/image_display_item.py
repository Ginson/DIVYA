
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QImage, QPixmap
import numpy as np

class ImageDisplayItem(QGraphicsPixmapItem):
    """A QGraphicsItem that can display a NumPy image array."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_image(self, image_data: np.ndarray):
        """
        Sets the image to be displayed from a NumPy array.
        Handles different image formats (grayscale, RGB).
        """
        if image_data is None:
            # Clear the pixmap if the image is None
            self.setPixmap(QPixmap())
            return

        # --- Convert NumPy array to QImage ---
        if len(image_data.shape) == 2:  # Grayscale
            height, width = image_data.shape
            bytes_per_line = width
            q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        elif len(image_data.shape) == 3:  # Color (assuming BGR for OpenCV)
            height, width, channel = image_data.shape
            bytes_per_line = 3 * width
            q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        else:
            print("Error: Unsupported image format.")
            return

        # --- Convert QImage to QPixmap and display ---
        pixmap = QPixmap.fromImage(q_image)
        self.setPixmap(pixmap)
