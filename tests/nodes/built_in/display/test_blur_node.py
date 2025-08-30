import unittest
import numpy as np
from nodes.built_in.display.blur_node import BlurNode

class TestBlurNode(unittest.TestCase):
    def test_blur_functionality(self):
        node = BlurNode()
        # Create a simple black image
        input_image = np.zeros((10, 10), dtype=np.uint8)
        
        # Execute the node
        result = node.execute(image=input_image)
        output_image = result.get("image")

        self.assertIsNotNone(output_image)
        self.assertEqual(input_image.shape, output_image.shape)

    def test_blur_with_kernel_size_param(self):
        node = BlurNode()
        node.set_param_value("kernel_size", 7)
        input_image = np.zeros((20, 20), dtype=np.uint8)
        
        result = node.execute(image=input_image)
        output_image = result.get("image")

        self.assertIsNotNone(output_image)

    def test_no_input_image(self):
        node = BlurNode()
        result = node.execute(image=None)
        self.assertIsNone(result.get("image"))

if __name__ == '__main__':
    unittest.main()
