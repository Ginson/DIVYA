import unittest
import numpy as np
from nodes.built_in.filters.canny_edge import CannyNode


class TestCannyEdgeFilter(unittest.TestCase):
    def test_edge_detection(self):
        node = CannyNode()
        # Create a test image with a clear edge (e.g., half black, half white)
        input_image = np.zeros((100, 100), dtype=np.uint8)
        input_image[:, 50:] = 255

        result = node.execute(image=input_image)
        output_image = result.get("image")

        self.assertIsNotNone(output_image)
        self.assertEqual(input_image.shape, output_image.shape)
        # Check if there are any white pixels (edges) detected
        self.assertGreater(np.sum(output_image), 0)

    def test_no_input_image(self):
        node = CannyNode()
        result = node.execute(image=None)
        self.assertIsNone(result.get("image"))


if __name__ == "__main__":
    unittest.main()
