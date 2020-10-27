
import uuid
import json
import struct
import pprint
from .company_identifiers import companyIdentifiers

class DictToObject(object):
    def __init__(self, dictionary):
        def _traverse(key, element):
            if isinstance(element, dict):
                return key, DictToObject(element)
            else:
                return key, element
        try:
            # python 2.X
            objd = dict(_traverse(k, v) for k, v in dictionary.iteritems())
            self.__dict__.update(objd)
        except AttributeError:
            # python 3.X
            objd = dict(_traverse(k, v) for k, v in dictionary.items())
            self.__dict__.update(objd)

class MsdEvents(DictToObject):
    def __init__(self, dictionary):
        DictToObject.__init__(self, dictionary)
    def __str__(self):
        return json.dumps(self.__dict__).replace('"', '\'')
    def __repr__(self):
        return json.dumps(self.__dict__).replace('"', '\'')

class MsdAccelData(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return json.dumps(self.__dict__).replace('"', '\'')
    def __repr__(self):
        return json.dumps(self.__dict__).replace('"', '\'')

class Msd:

    def __init__(self, raw):
        self.raw = raw
        self.mfg = struct.unpack('H', bytes(self.raw[0:2]))[0]
        self.company = self.companyIdentifiers(self.mfg)
        if self.mfg == 0x06:
            self.microsoft()
        elif self.mfg == 0x4C:
            self.apple()
        else:
            self.altbeacon()
            self.ingics()

    def __repr__(self):
        return pprint.pformat(vars(self))

    @staticmethod
    def companyIdentifiers(mfg):
        if str(mfg) in companyIdentifiers:
            return companyIdentifiers[str(mfg)]['name']
        return None

    @staticmethod
    def microsoftType(typeId):
        if typeId == 1: return 'XBox One'
        elif typeId == 6: return 'Apple Phone'
        elif typeId == 7: return 'Apple iPad'
        elif typeId == 8: return 'Android device'
        elif typeId == 9: return 'Windows 10 Desktop'
        elif typeId == 11: return 'Windows 10 Phone'
        elif typeId == 12: return 'Linus device'
        elif typeId == 13: return 'Windows IoT'
        elif typeId == 14: return 'Surface Hub'
        else: return ''

    def microsoft(self):
        self.scenario = struct.unpack('B', bytes(self.raw[2:3]))[0]
        self.typeId = struct.unpack('B', bytes(self.raw[3:4]))[0] & 0x3F
        self.type = self.microsoftType(self.typeId)
        self.slat = bytes(self.raw[6:10]).hex().upper()
        self.deviceHash = bytes(self.raw[10:]).hex().upper()

    def apple(self):
        self.typeId = struct.unpack('B', bytes(self.raw[2:3]))[0]
        self.type = None
        if self.typeId == 0x02:
            self.type = 'iBeacon'
            self.uuid = str(uuid.UUID(bytes(self.raw[4:20]).hex())).upper()
            self.major = struct.unpack('>H', bytes(self.raw[20:22]))[0]
            self.minor = struct.unpack('>H', bytes(self.raw[22:24]))[0]
            self.tx = struct.unpack('b', bytes(self.raw[24:25]))[0]

    def altbeacon(self):
        if len(self.raw) > 4 and struct.unpack('H', bytes(self.raw[2:4]))[0] == 0xACBE:
            self.type = 'altBeacon'
            self.code = 0xACBE
            self.id = bytes(self.raw[4:24]).hex().upper()
            self.refrssi = struct.unpack('b', bytes(self.raw[24:25]))[0]
            self.mfgReserved = bytes(self.raw[25:]).hex().upper()

    ########  Ingics IBS Parser ###############################################

    bitButton = 0
    bitMoving = 1
    bitHall = 2
    bitFall = 3
    bitPIR = 4
    bitIR = 5
    bitMatt = 6

    def ingics_ibs(self):
        eventMapping = {
            'button': self.bitButton,
            'moving': self.bitMoving,
            'hall': self.bitHall,
            'fall': self.bitFall,
            'pir': self.bitPIR,
            'ir': self.bitIR,
            'matt': self.bitMoving
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
            0x14: { 'name': 'iBS03T', 'temp': True, 'humidity': True, 'events': [ 'button' ] },
            0x15: { 'name': 'iBS03T', 'temp': True, 'humidity': False, 'events': [ 'button' ] },
            0x16: { 'name': 'iBS03G', 'temp': False, 'humidity': False, 'events': [ 'button', 'moving', 'fall' ]},
            0x17: { 'name': 'iBS03TP', 'temp': True, 'humidity': True, 'events': [] },
            0x18: { 'name': 'iBS04i', 'temp': False, 'humidity': False, 'events': [ 'button' ] },
            0x19: { 'name': 'iBS04', 'temp': False, 'humidity': False, 'events': [ 'button' ] },
            0x20: { 'name': 'iRS02', 'temp': True, 'humidity': False, 'events': [ 'hall' ] },
            0x21: { 'name': 'iRS02TP', 'temp': True, 'humidity': True, 'events': [ 'hall' ] },
            0x22: { 'name': 'iRS02RG', 'temp': False, 'humidity': False, 'events': [ 'hall' ], 'accel': True },
            0x30: { 'name': 'iBS05', 'temp': False, 'humidity': False, 'events': [ 'button' ] },
            0x35: { 'name': 'iBS05T', 'temp': True, 'humidity': False, 'events': [ 'button' ] },
            0x36: { 'name': 'iBS05G', 'temp': False, 'humidity': False, 'events': [ 'button', 'moving', 'fall' ]},
        }

        subtype = struct.unpack('B', bytes(self.raw[13:14]))[0]
        eventFlag = struct.unpack('B', bytes(self.raw[6:7]))[0]

        self.company = 'Ingics'
        self.code = struct.unpack('H', bytes(self.raw[2:4]))[0]
        self.battery = struct.unpack('H', bytes(self.raw[4:6]))[0] / 100
        self.user = struct.unpack('H', bytes(self.raw[11:13]))[0]
        self.events = {}
        self.eventFlag = eventFlag

        feature = featureMapping.get(subtype)
        if feature is not None:
            self.type = feature['name']
            if feature['temp']:
                self.temperature = struct.unpack('<h', bytes(self.raw[7:9]))[0] / 100
            if feature['humidity']:
                # a special handling for iBS03TP
                if subtype == 0x17 or subtype == 0x21:
                    self.temperatureExt = struct.unpack('<h', bytes(self.raw[9:11]))[0] / 100
                else:
                    self.humidity = struct.unpack('<h', bytes(self.raw[9:11]))[0]
            for event in feature['events']:
                bitNo = eventMapping.get(event)
                if bitNo is not None:
                    self.events[event] = (eventFlag & (1 << bitNo) != 0)
            if 'accel' in feature and feature['accel']:
                self.accel = MsdAccelData(
                    struct.unpack('h', bytes(self.raw[7:9]))[0],
                    struct.unpack('h', bytes(self.raw[9:11]))[0],
                    struct.unpack('h', bytes(self.raw[11:13]))[0]
                )
        else:
            self.type = 'Unknown Tag'
        self.events = MsdEvents(self.events)

    @staticmethod
    def ingics_rs_type(subtype):
        if subtype == 0x01:  return 'iBS02PIR-RS'
        elif subtype == 0x02: return 'iBS02IR-RS'
        elif subtype == 0x04: return 'iBS02HM'
        else: return 'iBS02RS'

    def ingics_rs(self):
        subtype = struct.unpack('B', bytes(self.raw[13:14]))[0]
        eventFlag = struct.unpack('B', bytes(self.raw[6:7]))[0]
        self.company = 'Ingics'
        self.code = struct.unpack('H', bytes(self.raw[2:4]))[0]
        self.type = self.ingics_rs_type(subtype)
        self.battery = struct.unpack('<H', bytes(self.raw[4:6]))[0] / 100
        self.user = struct.unpack('<H', bytes(self.raw[11:13]))[0]
        self.eventFlag = eventFlag
        self.events = MsdEvents({
            'sensor': (eventFlag & 0x04) != 0x00,
            'boot': (eventFlag & 0x10) != 0x00
        })

    def ingics_rg(self):
        self.company = 'Ingics'
        # 5900 81BC -> iBS01RG
        # 0D00 81BC -> iBS03RG
        self.code = struct.unpack('H', bytes(self.raw[2:4]))[0]
        self.type = 'iBS01RG' if self.mfg == 0x59 else 'iBS03RG'
        battActFlag = struct.unpack('<H', bytes(self.raw[4:6]))[0]
        self.battery = (battActFlag & 0x0FFF) / 100
        self.evenFlag = (battActFlag & 0xF000) >> 12
        self.events = MsdEvents({
            'button': (battActFlag & 0x2000) != 0,
            'moving': (battActFlag & 0x1000) != 0
        })
        self.accels = [
            MsdAccelData(
                struct.unpack('<h', bytes(self.raw[6:8]))[0],
                struct.unpack('<h', bytes(self.raw[8:10]))[0],
                struct.unpack('<h', bytes(self.raw[10:12]))[0]
            ),
            MsdAccelData(
                struct.unpack('<h', bytes(self.raw[12:14]))[0],
                struct.unpack('<h', bytes(self.raw[14:16]))[0],
                struct.unpack('<h', bytes(self.raw[16:18]))[0]
            ),
            MsdAccelData(
                struct.unpack('<h', bytes(self.raw[18:20]))[0],
                struct.unpack('<h', bytes(self.raw[20:22]))[0],
                struct.unpack('<h', bytes(self.raw[22:24]))[0]
            )
        ]

    def ingics_ibs01(self):
        subtype = struct.unpack('B', bytes(self.raw[13:14]))[0]
        if subtype == 0xff or subtype == 0:
            # old iBS01 fw, subtype is not avaiable
            self.company = 'Ingics'
            self.code = struct.unpack('H', bytes(self.raw[2:4]))[0]
            self.battery = struct.unpack('<H', bytes(self.raw[4:6]))[0] / 100
            self.events = {}
            if len(self.raw) > 10 and self.raw[7] != 0xFF and self.raw[8] != 0xFF:
                self.type = 'iBS01T'
                self.temperature = struct.unpack('<h', bytes(self.raw[7:9]))[0] / 100
                self.humidity = struct.unpack('<h', bytes(self.raw[9:11]))[0]
            else:
                # others, I cannot detect the real type from payload
                # collect all posible event data
                eventFlag = struct.unpack('B', bytes(self.raw[6:7]))[0]
                self.type = 'iBS01'
                self.events = {
                    'button': (eventFlag & (1 << self.bitButton) != 0),
                    'moving': (eventFlag & (1 << self.bitMoving) != 0),
                    'hall': (eventFlag & (1 << self.bitHall) != 0),
                    'fall': (eventFlag & (1 << self.bitFall) != 0)
                }
            self.events = MsdEvents(self.events)
        else:
            self.ingics_ibs()

    def ingics(self):
        if len(self.raw) >= 4:
            code = struct.unpack('H', bytes(self.raw[2:4]))[0]
            if self.mfg == 0x59 and code == 0xBC80:
                # iBS01(H/G/T)
                self.ingics_ibs01()
            elif self.mfg == 0x59 and code == 0xBC81:
                # iBS01RG
                self.ingics_rg()
            elif self.mfg == 0x0D and code == 0xBC83:
                # iBS02/iBS03/iBS04
                self.ingics_ibs()
            elif self.mfg == 0x0D and code == 0xBC82:
                # iBS02 for RS
                self.ingics_rs()
            elif self.mfg == 0x0D and code == 0xBC81:
                # iBS03RG
                self.ingics_rg()
            elif self.mfg == 0x082C and code == 0xBC85:
                # iBS05
                self.ingics_ibs()
