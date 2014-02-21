"""
Extracted from: http://bit.ly/1bSSOPx
"""

import json

packets = {
    'disconnect': 0,
    'connect': 1,
    'heartbeat': 2,
    'message': 3,
    'json': 4,
    'event': 5,
    'ack': 6,
    'error': 7,
    'noop': 8
  }

reasons = [
    'transport not supported',
    'client not handshaken',
    'unauthorized'
]

advice = [
    'reconnect'
]

def encode_packet(packet):
    packet_type = str(packets[packet['type']])
    packet_id = str(packet.get('id', ''))
    packet_endpoint = packet.get('endpoint', '')
    packet_ack = packet.get('ack')
    packet_data = None

    if packet['type'] == 'message':
        if packet_data != '':
            packet_data = packet['data']

    elif packet['type'] == 'event':
        ev = {'name': packet['name']}

        if packet['args'] and len(packet['args']):
            ev['args'] = packet['args']

        packet_data = json.dumps(ev)

    encoded = [
        packet_type,
        packet_id + '+' if packet_ack else '',
        packet_endpoint
    ]

    if packet_data != None:
        encoded.append(packet_data)

    return ':'.join(encoded)

