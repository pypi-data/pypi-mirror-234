import unittest
import fireworks.client


class TestBasic(unittest.TestCase):
    def test_import(self):
        self.assertRegex(fireworks.client.__version__, r"^\d+\.\d+\.\d+([a]\d+)?$")


if __name__ == "__main__":
    unittest.main()
