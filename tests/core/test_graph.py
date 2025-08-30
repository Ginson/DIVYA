import unittest
from app.core.graph import Graph, Edge
from nodes.base_node import BaseNode

# A mock BaseNode for testing purposes
class MockNode(BaseNode):
    category = "Test"
    def __init__(self, node_id, name="Test Node"):
        super().__init__(name=name, inputs=[], outputs=[])
        self.id = node_id

    def execute(self, **kwargs):
        return {}

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.node1 = MockNode("node1")
        self.node2 = MockNode("node2")

    def test_add_node(self):
        self.graph.add_node(self.node1)
        self.assertIn("node1", self.graph.nodes)
        self.assertEqual(self.graph.nodes["node1"], self.node1)

    def test_add_duplicate_node_raises_error(self):
        self.graph.add_node(self.node1)
        with self.assertRaises(ValueError):
            self.graph.add_node(self.node1)

    def test_get_node(self):
        self.graph.add_node(self.node1)
        retrieved_node = self.graph.get_node("node1")
        self.assertEqual(retrieved_node, self.node1)
        self.assertIsNone(self.graph.get_node("non_existent_node"))

    def test_add_edge(self):
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge("node1", "output1", "node2", "input1")
        edge_id = "node1:output1->node2:input1"
        self.assertIn(edge_id, self.graph.edges)
        edge = self.graph.edges[edge_id]
        self.assertEqual(edge.source_node_id, "node1")
        self.assertEqual(edge.source_output_name, "output1")
        self.assertEqual(edge.target_node_id, "node2")
        self.assertEqual(edge.target_input_name, "input1")

    def test_add_edge_with_missing_node_raises_error(self):
        with self.assertRaises(KeyError):
            self.graph.add_edge("node1", "output1", "node2", "input1")

    def test_remove_node(self):
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge("node1", "output1", "node2", "input1")
        
        self.graph.remove_node("node1")
        
        self.assertNotIn("node1", self.graph.nodes)
        edge_id = "node1:output1->node2:input1"
        self.assertNotIn(edge_id, self.graph.edges)

    def test_remove_edge(self):
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        edge_id = "node1:output1->node2:input1"
        self.graph.add_edge("node1", "output1", "node2", "input1")
        
        self.graph.remove_edge(edge_id)
        self.assertNotIn(edge_id, self.graph.edges)

if __name__ == '__main__':
    unittest.main()