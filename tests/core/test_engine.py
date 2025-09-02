import unittest
from unittest.mock import MagicMock
from app.core.engine import Engine
from app.core.graph import Graph
from nodes.base_node import BaseNode


class MockNode(BaseNode):
    category = "Test"

    def __init__(self, node_id, name="Test Node"):
        super().__init__(name=name, inputs=[], outputs=[])
        self.id = node_id
        self.execute = MagicMock(return_value={})

    def execute(self, **kwargs):
        return self.execute(**kwargs)


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = Engine()
        self.graph = Graph()
        self.node1 = MockNode("node1", "Node 1")
        self.node2 = MockNode("node2", "Node 2")
        self.node3 = MockNode("node3", "Node 3")

    def test_topological_sort_linear(self):
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_node(self.node3)
        self.graph.add_edge("node1", "output", "node2", "input")
        self.graph.add_edge("node2", "output", "node3", "input")

        sorted_nodes = self.engine._topological_sort(self.graph)
        self.assertEqual(sorted_nodes, ["node1", "node2", "node3"])

    def test_topological_sort_with_cycle(self):
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge("node1", "output", "node2", "input")
        self.graph.add_edge("node2", "output", "node1", "input")  # Cycle

        sorted_nodes = self.engine._topological_sort(self.graph)
        self.assertEqual(sorted_nodes, [])

    def test_process_execution_order(self):
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_node(self.node3)
        self.graph.add_edge("node1", "output", "node2", "input")
        self.graph.add_edge("node2", "output", "node3", "input")

        self.engine.process(self.graph)

        # Check if execute was called in the correct order
        self.node1.execute.assert_called_once()
        self.node2.execute.assert_called_once()
        self.node3.execute.assert_called_once()

    def test_process_io_handling(self):
        # Mock execute to return a specific value
        self.node1.execute.return_value = {"output_data": 42}
        self.node2.execute.return_value = {"output_data": 84}

        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_node(self.node3)
        self.graph.add_edge("node1", "output_data", "node3", "input1")
        self.graph.add_edge("node2", "output_data", "node3", "input2")

        self.engine.process(self.graph)

        # Verify that node3 received the correct inputs
        self.node3.execute.assert_called_once_with(input1=42, input2=84)


if __name__ == "__main__":
    unittest.main()
