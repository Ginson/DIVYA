from PyQt6.QtWidgets import QGraphicsObject, QGraphicsTextItem
from PyQt6.QtGui import QColor, QBrush, QPen, QFont
from PyQt6.QtCore import QRectF, Qt
from app.node_editor.socket import Socket

class Node(QGraphicsObject):
    """A visual representation of a node in the graph."""
    def __init__(self, base_node, parent=None):
        super().__init__(parent)
        self.base_node = base_node
        self.width = 180
        self.height = 100
        self.edges = []
        
        # --- Appearance ---
        self.title_color = QColor("#FF6B6B")
        self.bg_color = QColor("#4A4A4A")
        self.pen_default = QPen(QColor("#CFCFCF"))
        self.pen_selected = QPen(QColor("#FFFFA6"), 2)
        self.brush_title = QBrush(self.title_color)
        self.brush_background = QBrush(self.bg_color)

        # --- UI Elements ---
        self._setup_ui()

        # --- Flags & Signals ---
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
        self.xChanged.connect(self.on_position_changed)
        self.yChanged.connect(self.on_position_changed)

    def add_edge(self, edge):
        """Adds an edge to this node's list of edges."""
        self.edges.append(edge)

    def on_position_changed(self):
        """Called when the node's position changes."""
        for edge in self.edges:
            edge.update_path()

    def _setup_ui(self):
        """Initializes the visual components of the node."""
        # --- Title ---
        self.title_item = QGraphicsTextItem(self.base_node.name, self)
        self.title_item.setDefaultTextColor(Qt.GlobalColor.white)
        self.title_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.title_item.setPos(10, 5)

        # --- Sockets ---
        self.inputs = []
        self.outputs = []
        
        y_pos = 40
        for i, name in enumerate(self.base_node.inputs):
            socket = Socket(self, i, name, socket_type='input')
            socket.setPos(0, y_pos)
            self.inputs.append(socket)
            y_pos += 20

        y_pos = 40
        for i, name in enumerate(self.base_node.outputs):
            socket = Socket(self, i, name, socket_type='output')
            socket.setPos(self.width, y_pos)
            self.outputs.append(socket)
            y_pos += 20

    def boundingRect(self) -> QRectF:
        """Defines the node's bounding box."""
        return QRectF(0, 0, self.width, self.height).normalized()

    def paint(self, painter, option, widget=None):
        """Draws the node."""
        # --- Shadow ---
        # (Implementation omitted for brevity)

        # --- Body ---
        path_body = QRectF(0, 0, self.width, self.height)
        painter.setBrush(self.brush_background)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.drawRoundedRect(path_body, 10, 10)

        # --- Title Bar ---
        path_title = QRectF(0, 0, self.width, 30)
        painter.setBrush(self.brush_title)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(path_title.adjusted(5, 5, -5, 0)) # Rounded top corners