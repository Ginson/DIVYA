import sys
import os
from PyQt6.QtWidgets import QApplication

# Add the project root to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app.main_window import MainWindow
from app.node_editor.node import Node
from nodes.built_in.display.load_image import LoadImageNode
from nodes.built_in.display.blur_node import BlurNode
from nodes.built_in.filters.canny_edge import CannyNode
from nodes.built_in.display.display_image import DisplayNode


def main():
    # --- GUI Setup ---
    app = QApplication(sys.argv)
    main_win = MainWindow()

    # --- Create and Add Nodes ---
    # 1. Create the underlying data nodes
    load_node_data = LoadImageNode()
    blur_node_data = BlurNode()
    canny_node_data = CannyNode()
    display_node_data = DisplayNode()

    # 2. Connect the DisplayNode's signal to the UI's display slot
    display_node_data.image_processed.connect(main_win.image_display.set_image)

    # 3. Add the data nodes to the logical graph
    main_win.graph.add_node(load_node_data)
    main_win.graph.add_node(blur_node_data)
    main_win.graph.add_node(canny_node_data)
    main_win.graph.add_node(display_node_data)

    # 3.5. Connect the nodes
    import sys


import os
from PyQt6.QtWidgets import QApplication

# Add the project root to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app.main_window import MainWindow


def main():
    # --- GUI Setup ---
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    main_win.graph.add_edge(
        blur_node_data.id, "image", canny_node_data.id, "image"
    )
    main_win.graph.add_edge(
        canny_node_data.id, "image", display_node_data.id, "image"
    )

    # 4. Create the visual representations
    load_node_ui = Node(load_node_data)
    load_node_data.ui_node = load_node_ui
    blur_node_ui = Node(blur_node_data)
    blur_node_data.ui_node = blur_node_ui
    canny_node_ui = Node(canny_node_data)
    canny_node_data.ui_node = canny_node_ui
    display_node_ui = Node(display_node_data)
    display_node_data.ui_node = display_node_ui

    # 5. Add the visual nodes to the scene
    main_win.graph_view.scene.addItem(load_node_ui)
    main_win.graph_view.scene.addItem(blur_node_ui)
    main_win.graph_view.scene.addItem(canny_node_ui)
    main_win.graph_view.scene.addItem(display_node_ui)

    # 6. Position the nodes
    load_node_ui.setPos(100, 100)
    blur_node_ui.setPos(400, 100)
    canny_node_ui.setPos(700, 100)
    display_node_ui.setPos(1000, 100)

    main_win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
