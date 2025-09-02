from PyQt6.QtWidgets import QGraphicsPathItem
from PyQt6.QtGui import QColor, QPen, QPainterPath
from PyQt6.QtCore import QPointF


class Edge(QGraphicsPathItem):
    """A visual representation of a connection between two sockets."""

    def __init__(self, start_socket, end_socket=None, parent=None):
        super().__init__(parent)
        self.start_socket = start_socket
        self.end_socket = end_socket

        # --- Appearance ---
        self._pen = QPen(QColor("#A0A0A0"))
        self._pen.setWidth(2)
        self.setPen(self._pen)

        if self.start_socket and self.end_socket:
            self.update_path()

    def update_path(self, end_pos_override=None):
        """Updates the curve of the edge based on socket positions."""
        path = QPainterPath()
        start_pos = self.start_socket.scenePos()

        end_pos = end_pos_override
        if end_pos is None and self.end_socket:
            end_pos = self.end_socket.scenePos()
        elif end_pos is None and not self.end_socket:
            return  # Cannot draw without an end point

        path.moveTo(start_pos)

        # --- Bezier Curve ---
        dx = end_pos.x() - start_pos.x()
        ctrl1 = start_pos + QPointF(dx * 0.5, 0)
        ctrl2 = end_pos - QPointF(dx * 0.5, 0)
        path.cubicTo(ctrl1, ctrl2, end_pos)

        self.setPath(path)
