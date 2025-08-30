
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor
from app.node_editor.socket import Socket
from app.node_editor.edge import Edge
from app.node_editor.node import Node

class GraphView(QGraphicsView):
    """A view for displaying and interacting with the node graph."""
    node_selected = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.scene.selectionChanged.connect(self.on_selection_changed)

        self.edge_drag_mode = False
        self.drag_edge = None
        self.drag_start_socket = None

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setInteractive(True)
        self.setAcceptDrops(True)

        self.scene.setBackgroundBrush(QColor(53, 53, 53))

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            node_name = event.mimeData().text()
            if node_name in self.window().node_classes:
                position = self.mapToScene(event.position().toPoint())
                self.add_node(self.window().node_classes[node_name], position)
                event.acceptProposedAction()

    def add_node(self, node_class, position):
        """Adds a new node to the graph view and the core graph."""
        main_window = self.window()
        base_node = node_class()
        main_window.graph.add_node(base_node)

        ui_node = Node(base_node)
        base_node.ui_node = ui_node
        self.scene.addItem(ui_node)
        ui_node.setPos(position)

        # Connect display node signal if it's a DisplayNode
        if base_node.name == "Display Image":
            base_node.image_processed.connect(main_window.image_display.set_image)

        return ui_node

    def mousePressEvent(self, event):
        """Handles the start of an edge drag."""
        item = self.itemAt(event.pos())
        if isinstance(item, Socket):
            self.edge_drag_mode = True
            self.drag_start_socket = item
            self.drag_edge = Edge(self.drag_start_socket, None)
            self.scene.addItem(self.drag_edge)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handles the dragging of an edge."""
        if self.edge_drag_mode:
            self.drag_edge.update_path(self.mapToScene(event.pos()))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handles the end of an edge drag."""
        if self.edge_drag_mode:
            self.edge_drag_mode = False
            
            self.drag_edge.setVisible(False)
            end_item = self.itemAt(event.pos())
            self.drag_edge.setVisible(True)

            valid_connection = (
                isinstance(end_item, Socket) and
                end_item != self.drag_start_socket and
                end_item.socket_type != self.drag_start_socket.socket_type
            )

            if valid_connection:
                self.drag_edge.end_socket = end_item
                self.drag_edge.update_path()

                start_socket = self.drag_start_socket if self.drag_start_socket.socket_type == 'output' else end_item
                end_socket = end_item if self.drag_start_socket.socket_type == 'output' else self.drag_start_socket
                
                start_socket.node.add_edge(self.drag_edge)
                end_socket.node.add_edge(self.drag_edge)

                main_window = self.window()
                main_window.add_edge_to_graph(start_socket, end_socket)

            else:
                self.scene.removeItem(self.drag_edge)
            
            self.drag_edge = None
            self.drag_start_socket = None
        else:
            super().mouseReleaseEvent(event)

    def drawBackground(self, painter: QPainter, rect):
        """Draws a grid background."""
        super().drawBackground(painter, rect)
        
        grid_size = 20
        left = int(rect.left()) - int(rect.left()) % grid_size
        top = int(rect.top()) - int(rect.top()) % grid_size
        
        light_pen = QPen(QColor(60, 60, 60))
        light_pen.setWidth(1)
        painter.setPen(light_pen)
        
        for x in range(left, int(rect.right()), grid_size):
            painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
        for y in range(top, int(rect.bottom()), grid_size):
            painter.drawLine(int(rect.left()), y, int(rect.right()), y)

        dark_pen = QPen(QColor(40, 40, 40))
        dark_pen.setWidth(2)
        painter.setPen(dark_pen)
        
        for x in range(left, int(rect.right()), grid_size * 10):
            painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
        for y in range(top, int(rect.bottom()), grid_size * 10):
            painter.drawLine(int(rect.left()), y, int(rect.right()), y)

    def on_selection_changed(self):
        """Handles when the selection in the scene changes."""
        selected_items = self.scene.selectedItems()
        if selected_items and isinstance(selected_items[0], Node):
            self.node_selected.emit(selected_items[0])
        else:
            self.node_selected.emit(None)

    def clear(self):
        """Clears the graph view."""
        self.scene.clear()
        if self.window():
            self.window().graph.clear()
