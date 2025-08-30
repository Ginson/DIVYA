import unittest
from unittest.mock import patch
import numpy as np
import cv2
from nodes.built_in.display.load_image import LoadImageNode

class TestLoadImage(unittest.TestCase):

    @patch('cv2.imread')
    def test_load_image_success(self, mock_imread):
        # Mock cv2.imread to return a dummy image
        dummy_image = np.zeros((50, 50), dtype=np.uint8)
        mock_imread.return_value = dummy_image

        node = LoadImageNode()
        node.set_param_value("path", "dummy/path/image.png")
        
        result = node.execute()
        output_image = result.get("image")

        self.assertIsNotNone(output_image)
        self.assertEqual(output_image.shape, (50, 50))
        mock_imread.assert_called_once_with("dummy/path/image.png", cv2.IMREAD_GRAYSCALE)

    @patch('cv2.imread')
    def test_load_image_failure(self, mock_imread):
        # Mock cv2.imread to simulate a failure
        mock_imread.return_value = None

        node = LoadImageNode()
        node.set_param_value("path", "bad/path/image.png")

        result = node.execute()
        output_image = result.get("image")

        self.assertIsNotNone(output_image)
        # Should return a 10x10 black image as a fallback
        self.assertEqual(output_image.shape, (10, 10))
        self.assertTrue(np.all(output_image == 0))

if __name__ == '__main__':
    unittest.main()