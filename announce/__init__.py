__version__ = '0.0.4'
VERSION = __version__


import json
import uuid
import redis

from announce.packet import encode as encode_packet


class Announce(object):
    def __init__(self, *args, **kwargs):
        self.node_id = str(int(uuid.uuid4()))[:9]

        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 6379)
        db = kwargs.get('db', 0)
        password = kwargs.get('password', None)
        json_dumps = kwargs.get('json_dumps', json.dumps)

        self._test_mode = kwargs.get('_test_mode', False)

        if self._test_mode:
            self.client = None
        else:
            self.client = redis.StrictRedis(
                host=host, port=port, db=db, password=password)

        _namespace = kwargs.get('namespace', '')
        self.namespace = '/{0}'.format(_namespace) if _namespace != '' else ''

        self.room = ''
        self.volatile = None

        self.pack = json_dumps


    def send(self, data, room=None):
        if room:
            self.room = self.namespace + '/{0}'.format(room)
        elif self.namespace:
            self.room = self.namespace

        _packet = {
            'type': 'message',
            'data': data
        }

        return self.packet(_packet)


    def emit(self, event_name, data, room=None):
        if room:
            self.room = self.namespace + '/{0}'.format(room)
        elif self.namespace:
            self.room = self.namespace

        packet = {
            'type': 'event',
            'name': event_name,
            'args': [data]
        }

        return self.packet(packet)


    def packet(self, packet):
        packet['endpoint'] = self.namespace if self.namespace != '' else ''

        _packet = encode_packet(packet, json_dumps=self.pack)
        volatile = self.volatile
        exceptions = []

        return self.publish('dispatch', self.room, _packet, volatile, exceptions)


    def publish(self, name, *args):
        pack = self.pack({'nodeId': self.node_id, 'args': args})

        if not self._test_mode:
            self.client.publish(name, pack)

        return pack


if __name__ == '__main__':
    """
    Sample usage
    """
    a = Announce()
    a.emit('alert', {'msg': 'This is Hello'})
    a.emit('alert', {'msg': 'This is Hello'}, room='room')
    a.send('Alow')
    a.send('Alow', room='room')

    b = Announce(namespace='/namespace')
    b.emit('alert', {'msg': 'This is Hello'})
    b.emit('alert', {'msg': 'This is Hello'}, room='room')
    b.send('Alow')
    b.send('Alow', room='room')
