import yaml
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSplitter,
    QGraphicsView,
    QGraphicsScene,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from app.node_editor.graph_view import GraphView
from app.core.graph import Graph
from app.core.engine import Engine
from app.node_editor.image_display_item import ImageDisplayItem
from app.node_discovery import get_node_classes
from app.node_editor.node import Node
from app.node_editor.node_list_widget import NodeListWidget


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing Pipeline")
        self.setGeometry(100, 100, 1600, 900)

        # --- Core Logic ---
        self.graph = Graph()
        self.engine = Engine()
        self.node_classes = get_node_classes()

        # --- UI Setup ---
        self.init_ui()

    def init_ui(self):
        """Initializes the user interface."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Top Bar for Controls ---
        top_bar = QWidget()
        top_bar.setFixedHeight(40)
        top_bar_layout = QHBoxLayout(top_bar)
        self.run_button = QPushButton("Execute Graph")
        self.run_button.clicked.connect(self.execute_graph)
        self.save_button = QPushButton("Save Pipeline")
        self.save_button.clicked.connect(self.save_pipeline)
        self.load_button = QPushButton("Load Pipeline")
        self.load_button.clicked.connect(self.load_pipeline)
        top_bar_layout.addWidget(self.run_button)
        top_bar_layout.addWidget(self.save_button)
        top_bar_layout.addWidget(self.load_button)
        top_bar_layout.addStretch()
        main_layout.addWidget(top_bar)

        # --- Main Content Area (Splitter) ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # --- Node List (Left Side) ---
        self.node_list_widget = NodeListWidget(self.node_classes)
        splitter.addWidget(self.node_list_widget)

        # --- Node Editor (Middle) ---
        self.graph_view = GraphView(self)
        splitter.addWidget(self.graph_view)

        # --- Image Display (Right Side) ---
        self.image_view = QGraphicsView(self)
        self.image_scene = QGraphicsScene(self)
        self.image_view.setScene(self.image_scene)
        self.image_display = ImageDisplayItem()
        self.image_scene.addItem(self.image_display)
        splitter.addWidget(self.image_view)

        # --- Properties Panel (Far Right Side) ---
        from app.node_editor.properties_panel import PropertiesPanel

        self.properties_panel = PropertiesPanel(self)
        splitter.addWidget(self.properties_panel)

        # --- Connect Signals ---
        self.graph_view.node_selected.connect(self.properties_panel.set_node)

        # Set initial sizes for the splitter
        splitter.setSizes([200, 800, 400, 200])

    def execute_graph(self):
        """Executes the current graph."""
        print("--- MainWindow: Requesting Graph Execution ---")
        self.engine.process(self.graph)
        print(f"Graph state: {self.graph}")

    def add_edge_to_graph(self, start_socket, end_socket):
        """Adds a logical edge to the core graph."""
        source_node_id = start_socket.node.base_node.id
        source_output_name = start_socket.socket_name
        target_node_id = end_socket.node.base_node.id
        target_input_name = end_socket.socket_name

        print(
            f"UI: Adding edge from {source_node_id}:{source_output_name} to "
            f"{target_node_id}:{target_input_name}"
        )
        self.graph.add_edge(
            source_node_id,
            source_output_name,
            target_node_id,
            target_input_name,
        )
        self.execute_graph()

    def save_pipeline(self):
        """Saves the current pipeline to a YAML file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Pipeline", "", "YAML Files (*.yaml *.yml)"
        )
        if file_path:
            graph_data = self.graph.serialize()
            with open(file_path, "w") as f:
                yaml.dump(graph_data, f, default_flow_style=False)
            print(f"Pipeline saved to {file_path}")

    def load_pipeline(self):
        """Loads a pipeline from a YAML file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Pipeline", "", "YAML Files (*.yaml *.yml)"
        )
        if file_path:
            # Add a constructor to handle Python tuples
            def tuple_constructor(loader, node):
                return tuple(loader.construct_sequence(node))

            yaml.add_constructor(
                "tag:yaml.org,2002:python/tuple",
                tuple_constructor,
                Loader=yaml.SafeLoader,
            )

            with open(file_path, "r") as f:
                graph_data = yaml.safe_load(f)

            self.graph_view.clear()
            self.graph.deserialize(graph_data, self.node_classes)

            # Recreate the UI
            for node_id, base_node in self.graph.nodes.items():
                ui_node = Node(base_node)
                base_node.ui_node = (
                    ui_node  # Link the base node to the ui node
                )
                self.graph_view.scene.addItem(ui_node)
                if hasattr(base_node, "temp_pos"):
                    ui_node.setPos(
                        base_node.temp_pos[0], base_node.temp_pos[1]
                    )

                # Connect display node signal if it's a DisplayNode
                if base_node.name == "Display Image":
                    base_node.image_processed.connect(
                        self.image_display.set_image
                    )

            # Recreate the edges
            for edge_data in graph_data["edges"]:
                source_node = self.graph.get_node(edge_data["source_node_id"])
                target_node = self.graph.get_node(edge_data["target_node_id"])
                if source_node and target_node:
                    # Find the sockets
                    source_socket = None
                    for socket in source_node.ui_node.outputs:
                        if (
                            socket.socket_name
                            == edge_data["source_output_name"]
                        ):
                            source_socket = socket
                            break

                    target_socket = None
                    for socket in target_node.ui_node.inputs:
                        if (
                            socket.socket_name
                            == edge_data["target_input_name"]
                        ):
                            target_socket = socket
                            break

                    if source_socket and target_socket:
                        from app.node_editor.edge import Edge

                        edge = Edge(source_socket, target_socket)
                        source_socket.node.add_edge(edge)
                        target_socket.node.add_edge(edge)
                        self.graph_view.scene.addItem(edge)

            self.execute_graph()
