import unittest
from unittest.mock import Mock
import numpy as np
from nodes.built_in.display.display_image import DisplayNode


class TestDisplayImage(unittest.TestCase):
    def test_image_display_signal(self):
        node = DisplayNode()
        # Create a mock slot to connect to the signal
        mock_slot = Mock()
        node.image_processed.connect(mock_slot)

        # Create a test image
        test_image = np.ones((10, 10), dtype=np.uint8)

        # Execute the node
        node.execute(image=test_image)

        # Assert that the signal was emitted once with the correct data
        mock_slot.assert_called_once()
        # Check the argument of the first call
        self.assertTrue(np.array_equal(mock_slot.call_args[0][0], test_image))

    def test_no_input_image(self):
        node = DisplayNode()
        mock_slot = Mock()
        node.image_processed.connect(mock_slot)

        node.execute(image=None)

        # When input is None, it should emit an empty array
        mock_slot.assert_called_once()
        self.assertEqual(mock_slot.call_args[0][0].size, 0)


if __name__ == "__main__":
    unittest.main()
