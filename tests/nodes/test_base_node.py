import unittest
from nodes.base_node import BaseNode


# A concrete implementation of BaseNode for testing
class ConcreteNode(BaseNode):
    def __init__(self, name, inputs, outputs, parameters=None):
        super().__init__(name, inputs, outputs, parameters)

    def execute(self, **kwargs) -> dict:
        return {"result": 42}


class TestBaseNode(unittest.TestCase):
    def test_initialization(self):
        node = ConcreteNode(
            name="Test Node",
            inputs=["in1"],
            outputs=["out1"],
            parameters={"p1": 10},
        )
        self.assertIsNotNone(node.id)
        self.assertEqual(node.name, "Test Node")
        self.assertEqual(node.inputs, ["in1"])
        self.assertEqual(node.outputs, ["out1"])
        self.assertEqual(node.param_values, {"p1": 10})

    def test_set_param_value(self):
        node = ConcreteNode("Test", [], [], {"p1": 10})
        node.set_param_value("p1", 25)
        self.assertEqual(node.param_values["p1"], 25)

    def test_set_nonexistent_param_raises_keyerror(self):
        node = ConcreteNode("Test", [], [], {"p1": 10})
        with self.assertRaises(KeyError):
            node.set_param_value("nonexistent", 123)

    def test_repr(self):
        node = ConcreteNode("MyNode", [], [], {})
        self.assertIn("MyNode", repr(node))
        self.assertIn(node.id, repr(node))


if __name__ == "__main__":
    unittest.main()
