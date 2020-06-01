import re
import json
import struct

class PayloadParser:

    @staticmethod
    def findMsd(payload):
        payloadBytes = bytearray.fromhex(payload)
        i = 0
        length = len(payloadBytes)
        while i < length:
            packetLength = payloadBytes[i]
            packetType = payloadBytes[i + 1]
            if packetType == 0xFF:
                return payloadBytes[i + 2 : i + packetLength + 1]
            i += packetLength + 1
        return None

    bitButton = 0
    bitMoving = 1
    bitHall = 2
    bitFall = 3
    bitPIR = 4
    bitIR = 5
    bitMatt = 6

    @staticmethod
    def parseIBS01(msdBytes, mfgCode):
        subtype = struct.unpack('B', bytes(msdBytes[13:14]))[0]
        if subtype == 0xff or subtype == 0:
            # old iBS01 fw, subtype is not avaiable
            result = {
                'mfg': 'Ingics',
                'mfgCode': mfgCode,
                'battery': struct.unpack('<H', bytes(msdBytes[4:6]))[0],
                'events': {},
                'raw': ''.join(format(x, '02X') for x in msdBytes)
            }
            if len(msdBytes) > 10 and msdBytes[7] != 0xFF and msdBytes[8] != 0xFF:
                result['type'] = 'iBS01T'
                result['temperature'] = struct.unpack('<h', bytes(msdBytes[7:9]))[0]
                result['humidity'] = struct.unpack('<h', bytes(msdBytes[9:11]))[0]
            else:
                # others, I cannot detect the real type from payload
                # collect all posible event data
                eventFlag = struct.unpack('B', bytes(msdBytes[6:7]))[0]
                result['type'] = 'iBS01(H/G)'
                result['events'] = {
                    'button': (eventFlag & (1 << PayloadParser.bitButton) != 0),
                    'moving': (eventFlag & (1 << PayloadParser.bitMoving) != 0),
                    'hall': (eventFlag & (1 << PayloadParser.bitHall) != 0),
                    'fall': (eventFlag & (1 << PayloadParser.bitFall) != 0)
                }
            return result
        else:
            return PayloadParser.parseIBS(msdBytes, mfgCode)

    @staticmethod
    def parseIBS(msdBytes, mfgCode):
        eventMapping = {
            'button': PayloadParser.bitButton,
            'moving': PayloadParser.bitMoving,
            'hall': PayloadParser.bitHall,
            'fall': PayloadParser.bitFall,
            'pir': PayloadParser.bitPIR,
            'ir': PayloadParser.bitIR,
            'matt': PayloadParser.bitMoving
        }
        featureMapping = {
            0x01: { 'name': 'iBS02PIR', 'temp': False, 'humidity': False, 'events': [ 'pir' ] },
            0x02: { 'name': 'iBS02IR', 'temp': False, 'humidity': False, 'events': [ 'ir' ] },
            0x03: { 'name': 'iBS01', 'temp': False, 'humidity': False, 'events': [] },
            0x04: { 'name': 'iBS01H', 'temp': False, 'humidity': False, 'events': [ 'hall' ] },
            0x05: { 'name': 'iBS01T', 'temp': True, 'humidity': True, 'events': [] },
            0x06: { 'name': 'iBS01G', 'temp': False, 'humidity': False, 'events': [ 'moving', 'fall' ] },
            0x07: { 'name': 'iBS01T', 'temp': True, 'humidity': False, 'events': [] },
            0x10: { 'name': 'iBS03', 'temp': False, 'humidity': False, 'events': [ 'button', 'hall' ] },
            0x15: { 'name': 'iBS03T', 'temp': True, 'humidity': False, 'events': [ 'button' ] },
            0x16: { 'name': 'iBS03G', 'temp': False, 'humidity': False, 'events': [ 'button', 'moving', 'fall' ]},
            0x17: { 'name': 'iBS03TP', 'temp': True, 'humidity': True, 'events': [] },
            0x18: { 'name': 'iBS04i', 'temp': False, 'humidity': False, 'events': [] },
            0x19: { 'name': 'iBS04', 'temp': False, 'humidity': False, 'events': [] },
            0x01: { 'name': 'iRS02', 'temp': True, 'humidity': False, 'events': [ 'hall' ] }
        }

        result = {
            'mfg': 'Ingics',
            'mfgCode': mfgCode,
            'battery': struct.unpack('<H', bytes(msdBytes[4:6]))[0],
            'user': struct.unpack('<H', bytes(msdBytes[11:13]))[0],
            'events': {},
            'raw': ''.join(format(x, '02X') for x in msdBytes)
        }
        subtype = struct.unpack('B', bytes(msdBytes[13:14]))[0]
        eventFlag = struct.unpack('B', bytes(msdBytes[6:7]))[0]

        feature = featureMapping.get(subtype)
        if feature is not None:
            result['type'] = feature['name']
            if feature['temp']:
                result['temperature'] = struct.unpack('<h', bytes(msdBytes[7:9]))[0]
            if feature['humidity']:
                # a special handling for iBS03TP
                key = 'humidity' if subtype != 0x17 else 'temperature_ext'
                result[key] = struct.unpack('<h', bytes(msdBytes[9:11]))[0]
            for event in feature['events']:
                bitNo = eventMapping.get(event)
                if bitNo is not None:
                    result['events'][event] = eventFlag & (1 << bitNo)
        else:
            result['type'] = 'Unknown Tag'

        return result

    @staticmethod
    def parseIBSXXRG(msdBytes, mfgCode, beaconType):
        battActFlag = struct.unpack('<H', bytes(msdBytes[4:6]))[0]
        return {
            'mfg': 'Ingics',
            'mfgCode': mfgCode,
            'type': beaconType,
            'battery': (battActFlag & 0x3FFF),
            'events': {
                'button': (battActFlag & 0x8000) != 0,
                'moving': (battActFlag & 0x4000) != 0
            },
            'accel': [
                {
                    'x': struct.unpack('<h', bytes(msdBytes[6:8]))[0],
                    'y': struct.unpack('<h', bytes(msdBytes[8:10]))[0],
                    'z': struct.unpack('<h', bytes(msdBytes[10:12]))[0]
                },
                {
                    'x': struct.unpack('<h', bytes(msdBytes[12:14]))[0],
                    'y': struct.unpack('<h', bytes(msdBytes[14:16]))[0],
                    'z': struct.unpack('<h', bytes(msdBytes[16:18]))[0]
                },
                {
                    'x': struct.unpack('<h', bytes(msdBytes[18:20]))[0],
                    'y': struct.unpack('<h', bytes(msdBytes[20:22]))[0],
                    'z': struct.unpack('<h', bytes(msdBytes[22:24]))[0]
                }
            ],
            'raw': ''.join(format(x, '02X') for x in msdBytes)
        }

    @staticmethod
    def parseIBSRS(msdBytes, mfgCode):
        subtype = struct.unpack('B', bytes(msdBytes[13:14]))[0]
        eventFlag = struct.unpack('B', bytes(msdBytes[6:7]))[0]
        return {
            'mfg': 'Ingice',
            'mfgCode': mfgCode,
            'type': '??',
            'battery': struct.unpack('<H', bytes(msdBytes[4:6]))[0],
            'user': struct.unpack('<H', bytes(msdBytes[11:13]))[0],
            'events': {
                'sensor': (eventFlag & 0x04) != 0
            },
            'raw': ''.join(format(x, '02X') for x in msdBytes)
        }

    @staticmethod
    def parseMsd(msdBytes):
        mfg = struct.unpack('<H', bytes(msdBytes[0:2]))[0]
        type = struct.unpack('<H', bytes(msdBytes[2:4]))[0]
        # print(format(mfg, '04X'))
        # print(format(type, '04X'))
        if mfg == 0x59 and type == 0xBC80:
            # iBS01(H/G/T)
            return PayloadParser.parseIBS01(msdBytes, mfg)
        elif mfg == 0x59 and type == 0xBC81:
            # iBS01RG
            return PayloadParser.parseIBSXXRG(msdBytes, mfg, 'iBS01RG')
        elif mfg == 0x0D and type == 0xBC83:
            # iBS02/iBS03/iBS04
            return PayloadParser.parseIBS(msdBytes, mfg)
        elif mfg == 0x0D and type == 0xBC82:
            # iBS02 for RS
            return PayloadParser.parseIBSRS(msdBytes, mfg)
        elif mfg == 0x0D and type == 0xBC81:
            # iBS03RG
            return PayloadParser.parseIBSXXRG(msdBytes, mfg, 'iBS03RG')
        else:
            raise Exception('Not Ingics MSD format')

    @staticmethod
    def parse(payload):
        msdBytes = PayloadParser.findMsd(payload)
        return PayloadParser.parseMsd(msdBytes)

if __name__ == '__main__':
    payload = '02010612FF0D0083BC1401009611FFFFFFFF15000000'
    print(PayloadParser.parse(payload))
