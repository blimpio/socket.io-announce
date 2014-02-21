import json

packets = [
    'disconnect',
    'connect',
    'heartbeat',
    'message',
    'json',
    'event',
    'ack',
    'error',
    'noop'
]

reasons = [
    'transport not supported',
    'client not handshaken',
    'unauthorized'
]

advice = [
    'reconnect'
]

def encode_packet(packet):
    packet_type = str(packets.index(packet['type']))
    packet_id = str(packet.get('id', ''))
    packet_endpoint = packet.get('endpoint', '')
    packet_ack = packet.get('ack')
    packet_data = None

    if packet['type'] == 'event':
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

