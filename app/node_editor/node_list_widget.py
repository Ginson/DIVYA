
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag

class NodeListWidget(QTreeWidget):
    def __init__(self, node_classes, parent=None):
        super().__init__(parent)
        self.node_classes = node_classes
        self.setHeaderLabel("Available Nodes")
        self.setDragEnabled(True)
        self.populate_nodes()

    def populate_nodes(self):
        categories = {}
        for node_name, node_class in self.node_classes.items():
            category = node_class().category
            if category not in categories:
                categories[category] = []
            categories[category].append(node_name)

        for category, node_names in sorted(categories.items()):
            category_item = QTreeWidgetItem(self, [category])
            for node_name in sorted(node_names):
                node_item = QTreeWidgetItem(category_item, [node_name])
                node_item.setData(0, Qt.ItemDataRole.UserRole, node_name) # Store node name

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item and item.parent(): # Ensure it's a node, not a category
            node_name = item.data(0, Qt.ItemDataRole.UserRole)
            
            mime_data = QMimeData()
            mime_data.setText(node_name) # Set the node name as text data
            
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(supportedActions)
