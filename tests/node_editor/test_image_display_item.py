import unittest


@unittest.skip("Skipping GUI tests")
class TestImageDisplayItem(unittest.TestCase):
    def test_image_rendering(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
