import re
import json
from .payload_parser import PayloadParser

class MessageParser:

    @staticmethod
    def parseSingleMessage(msg):
        match = re.match('^\\$(.+),([0-9a-fA-F]{12}),([0-9a-fA-F]{12}),(-?\\d+),([0-9a-fA-F]+)(,(.+))?', msg)
        if match:
            data = {
                'type': match.group(1),
                'beacon': match.group(2),
                'gateway': match.group(3),
                'rssi': int(match.group(4)),
                'payload': match.group(5)
            }
            try:
                data['parsedPayload'] = PayloadParser.parse(data['payload'])
            except Exception as e:
                data['parsedPayload'] = e.message
            return data
        return None

    @staticmethod
    def parse(message, callback):
        try:
            data = json.load(message).data
        except:
            data = re.split('\\r?\\n', message)
        index = 0
        for msg in data:
            callback(MessageParser.parseSingleMessage(msg), index)
            index += 1

if __name__ == '__main__':
    def cb(data, index):
        print('#{0}: {1}'.format(index, data))
    message = '$GPRP,A8F9F2190E7A,A99213AA86EF,-77,02010612FF0D0083BCD60000FFFFFFFFFFFF15000000'
    MessageParser.parse(message, cb)
