import unittest
from announce import Announce

class TestAnnounce(unittest.TestCase):
    def setUp(self):
        self.announce = Announce(_debug_mode=True)

    def test_emit(self):
        sample = '"args": ["", "5:::{\\"name\\": \\"status\\", \\"args\\": [{\\"msg\\": \\"This is a test\\", \\"countdown\\": 1000}]}", null, []]'

        result = self.announce.emit(
            'status', {'msg': 'This is a test', 'countdown': 1000})

        self.assertIn(sample, result)


if __name__ == '__main__':
    unittest.main()
