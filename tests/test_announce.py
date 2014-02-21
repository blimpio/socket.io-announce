import unittest
import json

from announce import Announce

class TestAnnounce(unittest.TestCase):
    def setUp(self):
        self.announce = Announce(_debug_mode=True)

    def test_emit(self):
        expected = {'nodeId': '197520823', 'args': ['', '5:::{"name": "status", "args": [{"countdown": 1000, "msg": "This is a test"}]}', None, []]}

        result = json.loads(self.announce.emit(
            'status', {'msg': 'This is a test', 'countdown': 1000}))


        self.assertEqual(expected['args'][0], result['args'][0])
        self.assertEqual(len(expected['args'][1]), len(result['args'][1]))
        self.assertEqual(expected['args'][1][:4], result['args'][1][:4])
        self.assertEqual(expected.keys(), result.keys())


if __name__ == '__main__':
    unittest.main()
