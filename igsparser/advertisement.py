import uuid
import json
import struct
import pprint
from .appearance import appearanceList
from .msd import Msd

class Advertisement:

    def __init__(self, payload):
        self.raw = bytearray.fromhex(payload)
        self.flags = None
        self.localName = None
        self.txPowerLevel = None
        self.manufacturerData = None
        self.serviceData = []
        self.serviceUuids = []
        self.serviceSolicitationUuids = []
        self.parse()

    def __repr__(self):
        return pprint.pformat(vars(self))

    def parse(self):
        i = 0
        length = len(self.raw)
        while i < length:
            adLength = self.raw[i]
            adType = self.raw[i + 1]
            adData = self.raw[i + 2 : i + adLength + 1]
            # Flags
            if adType == 0x01:
                self.flags = struct.unpack('B', bytes(adData))[0]
            # Complete List of 16-bit Service Class UUIDs
            elif adType == 0x03:
                adData.reverse()
                self.serviceUuids.append(bytes(adData).hex().upper())
            # Complete List of 128-bit Service Class UUIDs
            elif adType == 0x07:
                adData.reverse()
                self.serviceUuids.append(str(uuid.UUID(bytes(adData).hex())).upper())
            # Shortened Local Name
            # Complete Local Name
            elif adType == 0x08 or adType == 0x09:
                self.localName = adData.decode('utf-8')
            # Tx Power Level
            elif adType == 0x0A:
                self.txPowerLevel = struct.unpack('b', bytes(adData))[0]
            # Service Data - 16-bit UUID
            elif adType == 0x16:
                serviceUuid = struct.unpack('H', bytes(adData[0:2]))[0]
                serviceData = adData[2:]
                self.serviceData.append({
                    'uuid': serviceUuid,
                    'data': bytes(serviceData)
                })
                serviceData.reverse()
                if serviceUuid == 0x2AC3:
                    # org.bluetooth.characteristic.object_id
                    self.objectId = bytes(serviceData).hex().upper()
                elif serviceUuid == 0x2A6E:
                    # org.bluetooth.characteristic.temperature
                    self.temperature = struct.unpack('h', bytes(serviceData))[0] / 100
                    self.temperatureUnit = 'C'
                elif serviceUuid == 0x2A1F:
                    # org.bluetooth.unit.thermodynamic_temperature.degree_celsius
                    self.temperature = struct.unpack('h', bytes(serviceData))[0] / 10
                    self.temperatureUnit = 'C'
                elif serviceUuid == 0x2A20:
                    # org.bluetooth.unit.thermodynamic_temperature.degree_fahrenheit
                    self.temperature = struct.unpack('h', bytes(serviceData))[0] / 10
                    self.temperatureUnit = 'F'
                elif serviceUuid == 0x2A6F:
                    # org.bluetooth.characteristic.humidity
                    self.humidity = struct.unpack('h', bytes(serviceData))[0] / 100
            # List of 16-bit Service Solicitation UUIDs
            # List of 32-bit Service Solicitation UUIDs
            elif adType == 0x14 or adType == 0x1F:
                adData.reverse()
                self.serviceSolicitationUuids.append(bytes(adData).hex().upper())
            # List of 128 bit Service Solicitation UUIDs
            elif adType == 0x15:
                adData.reverse()
                self.serviceSolicitationUuids.append(str(uuid.UUID(bytes(adData).hex())).upper())
            # Appearance
            elif adType == 0x19:
                val = str(struct.unpack('H', bytes(adData))[0])
                self.apperance = apperanceList[val] if val in apperanceList else val
            # Service Data - 32-bit UUID
            elif adType == 0x20:
                serviceUuid = adData[0:4]
                serviceData = adData[4:]
                serviceUuid.reverse()
                serviceData.reverse()
                self.serviceData.append({
                    'uuid': bytes(serviceUuid).hex().upper(),
                    'data': bytes(serviceData).hex().upper()
                })
            # Service Data - 128-bit UUID
            elif adType == 0x21:
                serviceUuid = adData[0:16]
                serviceData = adData[16:]
                serviceUuid.reverse()
                serviceData.reverse()
                self.serviceData.append({
                    'uuid': str(uuid.UUID(bytes(serviceUuid).hex())).upper(),
                    'data': bytes(serviceData).hex().upper()
                })
            # Manufacturer Specific Data
            elif adType == 0xFF:
                self.manufacturerData = Msd(adData)
            i += adLength + 1
