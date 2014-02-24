import json
import uuid
import redis

from .packet import encode as encode_packet

class Announce(object):
    def __init__(self, *args, **kwargs):
        self.node_id = str(int(uuid.uuid4()))[:9]

        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 6379)
        db = kwargs.get('db', 0)
        password = kwargs.get('password', None)

        self._debug_mode = kwargs.get('_debug_mode', False)

        if self._debug_mode:
            self.client = None
        else:
            self.client = redis.StrictRedis(
                host=host, port=port, db=db, password=password)

        self.namespace = kwargs.get('namespace', '')
        self.room = ''
        self.volatile = None

        self.pack = json.dumps


    def send(self, data, room=None):
        if room:
            self.room = '/'.join([self.namespace, room])

        _packet = {
            'type': 'message',
            'data': data
        }

        return self.packet(_packet)


    def emit(self, event_name, data, room=None):
        if room:
            self.room = '/'.join([self.namespace, room])

        packet = {
            'type': 'event',
            'name': event_name,
            'args': [data]
        }

        return self.packet(packet)


    def packet(self, packet):
        packet['endpoint'] = self.namespace

        _packet = encode_packet(packet)
        volatile = self.volatile
        exceptions = []

        return self.publish('dispatch', self.room, _packet, volatile, exceptions)


    def publish(self, name, *args):
        pack = self.pack({'nodeId': self.node_id, 'args': args})

        if not self._debug_mode:
            self.client.publish(name, pack)

        return pack


if __name__ == '__main__':
    """
    Sample usage
    """
    a = Announce(host='162.243.214.116',
                 password='HLDTSmQUzkN2Zw5AaFDntwajLTvrWsFw@')

    a.emit('message', {'greeting': 'Hello World'}, room='u1')
    # a.emit('alert', {'msg': 'This is Hello'})
    # a.emit('alert', {'msg': 'This is Hello'}, room='room')
    # a.send('Alow')
    # a.send('Alow', room='room')


    # b = Announce(host='162.243.214.116',
    #              password='HLDTSmQUzkN2Zw5AaFDntwajLTvrWsFw@',
    #              namespace='/namespace')

    # b.emit('alert', {'msg': 'This is Hello'})
    # b.emit('alert', {'msg': 'This is Hello'}, room='room')
    # b.send('Alow')
    # b.send('Alow', room='room')

