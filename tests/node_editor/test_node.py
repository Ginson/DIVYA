import unittest


@unittest.skip("Skipping GUI tests")
class TestNode(unittest.TestCase):
    def test_node_properties(self):
        pass

    def test_node_behavior(self):
        pass


if __name__ == "__main__":
    unittest.main()
