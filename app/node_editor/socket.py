
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QColor, QBrush, QPen
from PyQt6.QtCore import QRectF

class Socket(QGraphicsItem):
    """A visual representation of an input or output socket on a node."""
    def __init__(self, parent_node, index, name, socket_type='output'):
        super().__init__(parent_node)
        self.node = parent_node
        self.index = index
        self.socket_name = name
        self.socket_type = socket_type
        
        self.radius = 6
        
        # --- Appearance ---
        self.brush = QBrush(QColor("#FFC666"))
        self.pen = QPen(QColor("#000000"))

    def boundingRect(self) -> QRectF:
        """Defines the socket's bounding box."""
        return QRectF(
            -self.radius, -self.radius,
            2 * self.radius, 2 * self.radius
        ).normalized()

    def paint(self, painter, option, widget=None):
        """Draws the socket."""
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(int(-self.radius), int(-self.radius), int(2 * self.radius), int(2 * self.radius))
