import json
import uuid
import redis

import parser

class Announce(object):
    def __init__(self, *args, **kwargs):
        self.node_id = int(uuid.uuid4())

        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 6379)
        db = kwargs.get('db', 0)
        password = kwargs.get('password', None)

        self.client = redis.StrictRedis(
            host=host, port=port, db=db, password=password)

        self.namespace = kwargs.get('namespace', '')
        self.volatile = True

        self.pack = json.dumps


    def emit(self, event_name, data):
        packet = {
            'type': 'event',
            'name': event_name,
            'args': data
        }

        return self.packet(packet)


    def packet(self, packet):
        packet['endpoint'] = self.namespace

        _packet = parser.encode_packet(packet)
        volatile = self.volatile
        exceptions = []

        self.publish('dispatch', self.namespace, _packet, volatile, exceptions)

    def publish(self, name, *args):
        pack = self.pack({'nodeId': self.node_id, 'args': args})
        print(pack)
        self.client.publish(name, pack)

if __name__ == '__main__':
    a = Announce()
    a.emit('alert', {'msg': 'This is Hello'})

