import unittest

@unittest.skip("Skipping GUI tests")
class TestSocket(unittest.TestCase):
    def setUp(self):
        pass

    def test_data_transfer(self):
        pass

    def test_connection_establishment(self):
        pass

    def test_connection_closure(self):
        pass

if __name__ == '__main__':
    unittest.main()
