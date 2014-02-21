import redis
import json
import uuid

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def emmit(room, event, data):
    node_id = int(uuid.uuid4())
    payload = {'name': event, 'args': [data]}

    packet = {
        'nodeId': node_id,
        'args': [
            '/{}'.format(room),
            '5:::{0}'.format(json.dumps(payload)),
            None,
            []
        ]
    }

    r.publish('dispatch', json.dumps(packet))


if __name__ == '__main__':
    room = 'a1'
    event = 'message'
    data = {
        'sender_id': 1,
        'data_type': 'notification',
        'method': 'create',
        'data': { }
    }

    emmit(room, event, data)
