import json
import uuid
import redis

import parser

class Announce(object):
    def __init__(self, *args, **kwargs):
        self.node_id = str(int(uuid.uuid4()))[:9]

        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 6379)
        db = kwargs.get('db', 0)
        password = kwargs.get('password', None)

        self.client = redis.StrictRedis(
            host=host, port=port, db=db, password=password)

        self.namespace = kwargs.get('namespace', '')
        self.room = ''
        self.volatile = None

        self.pack = json.dumps


    def send(self, data):
        _packet = {
            'type': 'message',
            'data': data
        }

        self.packet(_packet)


    def emit(self, event_name, data, to=None):
        if to:
            self.room = '/'.join([self.namespace, to])

        packet = {
            'type': 'event',
            'name': event_name,
            'args': data
        }

        self.packet(packet)


    def packet(self, packet):
        packet['endpoint'] = self.namespace

        _packet = parser.encode_packet(packet)
        volatile = self.volatile
        exceptions = []

        self.publish('dispatch', self.room, _packet, volatile, exceptions)


    def publish(self, name, *args):
        pack = self.pack({'nodeId': self.node_id, 'args': args})

        print(pack)

        self.client.publish(name, pack)


if __name__ == '__main__':
    """
    Sample usage
    """
    a = Announce()
    a.emit('alert', {'msg': 'This is Hello'})
    a.send('Alow')
    a.emit('alert', {'msg': 'This is Hello'}, to='room')

    b = Announce(namespace='/namespace')
    b.emit('alert', {'msg': 'This is Hello'})
    b.send('Alow')
    b.emit('alert', {'msg': 'This is Hello'}, to='room')

