import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from nodes.base_node import BaseNode
from app.node_discovery import get_node_classes


# --- Mock Node Classes ---
class MockBlurNode(BaseNode):
    category = "Filters"

    def __init__(self):
        super().__init__(name="Blur", inputs=["image"], outputs=["image"])

    def execute(self, **kwargs):
        return {}


class MockCannyNode(BaseNode):
    category = "Filters"

    def __init__(self):
        super().__init__(
            name="Canny Edge", inputs=["image"], outputs=["image"]
        )

    def execute(self, **kwargs):
        return {}


class MockDisplayNode(BaseNode):
    category = "Display"

    def __init__(self):
        super().__init__(name="Display Image", inputs=["image"], outputs=[])

    def execute(self, **kwargs):
        return {}


class MockLoadImageNode(BaseNode):
    category = "IO"

    def __init__(self):
        super().__init__(name="Load Image", inputs=[], outputs=["image"])

    def execute(self, **kwargs):
        return {}


class MockLoadColorImageNode(BaseNode):
    category = "IO"

    def __init__(self):
        super().__init__(name="Load Color Image", inputs=[], outputs=["image"])

    def execute(self, **kwargs):
        return {}


class MockGrayscaleNode(BaseNode):
    category = "Plugins"

    def __init__(self):
        super().__init__(name="Grayscale", inputs=["image"], outputs=["image"])

    def execute(self, **kwargs):
        return {}


class TestNodeDiscovery(unittest.TestCase):

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("importlib.import_module")
    def test_get_node_classes_discovery(
        self, mock_import, mock_isdir, mock_listdir
    ):
        # Simulate the directory structure and files
        mock_listdir.side_effect = [
            ["built_in", "plugins"],  # Top level
            ["display", "filters", "io"],  # Inside nodes
            ["display_image.py", "load_image.py"],  # Inside display
            ["canny_edge.py", "blur_node.py"],  # Inside filters
            ["load_image.py"],  # Inside io
            ["custom_grayscale_node.py"],  # Inside plugins
        ]
        mock_isdir.return_value = True

        def import_side_effect(module_name):
            mock_mod = MagicMock()
            if "blur_node" in module_name:
                mock_mod.BlurNode = MockBlurNode
            elif "canny_edge" in module_name:
                mock_mod.CannyNode = MockCannyNode
            elif "display_image" in module_name:
                mock_mod.DisplayNode = MockDisplayNode
            elif "nodes.built_in.display.load_image" in module_name:
                mock_mod.LoadImageNode = MockLoadImageNode
            elif "nodes.built_in.io.load_image" in module_name:
                mock_mod.LoadColorImageNode = MockLoadColorImageNode
            elif "custom_grayscale_node" in module_name:
                mock_mod.GrayscaleNode = MockGrayscaleNode
            return mock_mod

        mock_import.side_effect = import_side_effect

        node_classes = get_node_classes()

        # --- Assertions ---
        self.assertEqual(len(node_classes), 6)
        self.assertIn("Blur", node_classes)
        self.assertIn("Canny Edge", node_classes)
        self.assertIn("Display Image", node_classes)
        self.assertIn("Load Image", node_classes)
        self.assertIn("Load Color Image", node_classes)
        self.assertIn("Grayscale", node_classes)


if __name__ == "__main__":
    unittest.main()
