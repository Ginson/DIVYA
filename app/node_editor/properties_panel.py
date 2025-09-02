from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QFormLayout,
)
from PyQt6.QtCore import Qt


class PropertiesPanel(QWidget):
    """A panel to display and edit the parameters of a selected node."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Properties")
        self.setMinimumWidth(250)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel("No Node Selected")
        self.title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.main_layout.addWidget(self.title)

        # This layout will hold the dynamically generated parameter widgets
        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        self.current_node = None

    def set_node(self, node_item):
        """
        Updates the panel to show the properties of the given visual node item.
        """
        self.current_node = node_item
        self.clear_panel()

        if not self.current_node:
            self.title.setText("No Node Selected")
            return

        base_node = self.current_node.base_node
        self.title.setText(f"Properties: {base_node.name}")

        # Create widgets for each parameter
        for param_name, param_value in base_node.param_values.items():
            # For now, we'll use a simple QLineEdit for all types
            # In the future, we can use QSpinBox for ints, etc.
            editor = QLineEdit(str(param_value))

            # Connect the editor's change signal to a handler
            editor.textChanged.connect(
                # Use a lambda to capture the parameter name
                lambda text, name=param_name: self.on_param_changed(name, text)
            )

            self.form_layout.addRow(
                QLabel(param_name.replace("_", " ").title()), editor
            )

    def on_param_changed(self, param_name, new_value):
        """Handles when a parameter's value is changed in the UI."""
        if self.current_node:
            # Try to convert the value to the correct type (e.g., int, float)
            # This is a simple implementation; a more robust version would be needed for production
            try:
                original_type = type(
                    self.current_node.base_node.param_values[param_name]
                )
                converted_value = original_type(new_value)
                self.current_node.base_node.set_param_value(
                    param_name, converted_value
                )
                print(f"Set '{param_name}' to {converted_value}")
            except (ValueError, TypeError) as e:
                print(
                    f"Invalid value for '{param_name}': {new_value}. Error: {e}"
                )

    def clear_panel(self):
        """Removes all parameter editor widgets from the form."""
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)
