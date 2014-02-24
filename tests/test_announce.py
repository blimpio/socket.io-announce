import unittest
import json
import logging

log = logging.getLogger(__name__)

from announce import Announce

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.announce = Announce(_test_mode=True)

    def compare_payloads(self, expected, result_text):
        result = json.loads(result_text)

        self.assertEqual(expected.keys(), result.keys())

        attr_lenght = len(expected['args'])
        self.assertEqual(attr_lenght, len(result['args']))

        self.assertEqual(expected['args'][0], result['args'][0])
        self.assertEqual(expected['args'][2], result['args'][2])
        self.assertEqual(expected['args'][3], result['args'][3])

        expected_msg_parts = expected['args'][1].split(':', 3)
        result_msg_parts = result['args'][1].split(':', 3)

        self.assertEqual(expected_msg_parts[0], result_msg_parts[0])
        self.assertEqual(expected_msg_parts[1], result_msg_parts[1])
        self.assertEqual(expected_msg_parts[2], result_msg_parts[2])


    def check_json_payload(self, expected, result_text):
        result = json.loads(result_text)

        expected_msg_parts = expected['args'][1].split(':', 3)
        result_msg_parts = result['args'][1].split(':', 3)

        expected_payload = json.loads(expected_msg_parts[3])
        result_payload = json.loads(result_msg_parts[3])

        e_keys = sorted(expected_payload.keys())
        r_keys = sorted(result_payload.keys())

        self.assertEqual(e_keys, r_keys)

        for key in e_keys:
            self.assertEqual(expected_payload[key], result_payload[key])


class TestAnnounce(BaseTestCase):
    def test_emit(self):
        expected = {
            'nodeId': 197520823,
            'args': [
                '',
                '5:::{"name": "message", "args": [{"countdown": 1000, "msg": "This is a test"}]}',
                None,
                []
            ]
        }

        result_text = self.announce.emit('message',
            {'msg': 'This is a test', 'countdown': 1000})

        self.compare_payloads(expected, result_text)
        self.check_json_payload(expected, result_text)


    def test_send(self):
        expected = {
            'nodeId': 286326561,
            'args': [
                '',
                '3:::Hello, world!',
                None,
                []
            ]
        }

        result_text = self.announce.send('Hello, world!')

        self.compare_payloads(expected, result_text)


    def test_send_in_room(self):
        expected = {
            'nodeId': 286326561,
            'args': [
                '/room',
                '3:::Hello world!',
                None,
                []
            ]
        }

        result_text = self.announce.send('Hello world!', room='room')

        self.compare_payloads(expected, result_text)


    def test_emit_in_room(self):
        expected = {
            'nodeId': 286326561,
            'args': [
                '/room',
                '5:::{"name":"message","args":[{"user":"@dshaw"}]}',
                None,
                []
            ]
        }

        result_text = self.announce.emit('message', {'user': '@dshaw'}, room='room')

        self.compare_payloads(expected, result_text)
        self.check_json_payload(expected, result_text)


    def test_send_in_namespace(self):
        self.announce = Announce(_test_mode=True, namespace='namespace')

        expected = {
            'nodeId': 149241983,
            'args': [
                '/namespace',
                '3::/namespace:Hello world!',
                None,
                []
            ]
        }

        result_text = self.announce.send('Hello world!')

        self.compare_payloads(expected, result_text)


    def test_send_in_namespace_with_room(self):
        self.announce = Announce(_test_mode=True, namespace='namespace')

        expected = {
            'nodeId': 149241983,
            'args': [
                '/namespace/room',
                '3::/namespace:Hello world!',
                None,
                []
            ]
        }

        result_text = self.announce.send('Hello world!', room='room')

        self.compare_payloads(expected, result_text)


    def test_emit_in_namespace(self):
        self.announce = Announce(_test_mode=True, namespace='namespace')

        expected = {
            'nodeId': 149241983,
            'args': [
                '/namespace',
                '5::/namespace:{"name":"message","args":[{"user":"@dshaw"}]}',
                None,
                []
            ]
        }

        result_text = self.announce.emit('message', {'user': '@dshaw'})

        self.compare_payloads(expected, result_text)
        self.check_json_payload(expected, result_text)


    def test_emit_in_namespace_with_room(self):
        self.announce = Announce(_test_mode=True, namespace='namespace')

        expected = {
            'nodeId': 149241983,
            'args': [
                '/namespace/room',
                '5::/namespace:{"name":"message","args":[{"user":"@dshaw"}]}',
                None,
                []
            ]
        }

        result_text = self.announce.emit('message', {'user': '@dshaw'}, room='room')

        self.compare_payloads(expected, result_text)
        self.check_json_payload(expected, result_text)


if __name__ == '__main__':
    unittest.main()
