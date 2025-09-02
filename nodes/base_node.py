# file: nodes/base_node.py

from abc import ABC, abstractmethod, ABCMeta
import uuid
from typing import Any, Dict
from PyQt6.QtCore import QObject


# --- Metaclass for combining QObject and ABC ---
# This resolves the metaclass conflict between PyQt's QObject and Python's ABC
class QObjectABCMeta(type(QObject), ABCMeta):
    pass


class BaseNode(QObject, ABC, metaclass=QObjectABCMeta):
    """
    An abstract base class for all processing nodes in the graph.
    Inherits from QObject to support signals and ABC for abstract methods.
    """

    def __init__(
        self,
        name: str,
        inputs: list[str],
        outputs: list[str],
        parameters: Dict[str, Any] = None,
    ):
        """
        Initializes the node.
        """
        super().__init__()
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.inputs: list[str] = inputs
        self.outputs: list[str] = outputs

        self.param_values: Dict[str, Any] = parameters if parameters else {}

    @abstractmethod
    def execute(self, **kwargs) -> dict:
        """
        The core processing logic of the node. Must be implemented by subclasses.
        """
        pass

    def set_param_value(self, param_name: str, value: Any):
        """Updates the value of a parameter."""
        if param_name in self.param_values:
            self.param_values[param_name] = value
        else:
            raise KeyError(
                f"Node '{self.name}' has no parameter named '{param_name}'."
            )

    def __repr__(self) -> str:
        """Provides a developer-friendly representation of the node."""
        return f"Node(name='{self.name}', id='{self.id}')"
