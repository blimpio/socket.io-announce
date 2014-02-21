import unittest

class TestAnnounce(unittest.TestCase):
    def setUp(self):
        print('setUp')

    def test_first(self):
        self.assertEqual(1, 1)
