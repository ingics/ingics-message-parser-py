# ingics-message-parser-py

Message parser for Ingics BLE beacon and gateway.


## Uasge

### Install

From github
```
pip install -U git+https://github.com/ingics/ingics-message-parser-py
```
From local clone
```
pip install .
```

### Run Unit Test
```
pip install .
pip install pytest
pytest -v
pytest -k <test key word>
```

### Bluepy

There is an example code for scanning iBS03T device in example folder.
The code has been tested on RPI3B+.

### Shell tools

#### parse_payload.py
Used to parse the advertisement payload from iBSXX series BLE Beacons.
For example:
```
bin/parse_payload.py 02010612FF0D0083BC230100E60A30000000140B0600
{'flags': 6,
 'localName': None,
 'manufacturerData': {'battery': 2.91,
 'code': 48259,
 'company': 'Ingics',
 'eventFlag': 0,
 'events': {'button': false, 'boot': false},
 'humidity': 48.0,
 'mfg': 13,
 'raw': bytearray(b'\r\x00\x83\xbc#\x01\x00\xe6\n0\x00\x00\x00\x14\x0b\x06'
                  b'\x00'),
 'temperature': 27.9,
 'type': 'iBS03T',
 'user': 0},
 'raw': bytearray(b'\x02\x01\x06\x12\xff\r\x00\x83\xbc#\x01\x00\xe6\n0\x00'
                  b'\x00\x00\x14\x0b\x06\x00'),
 'serviceData': [],
 'serviceSolicitationUuids': [],
 'serviceUuids': [],
 'txPowerLevel': None}
```

#### parse_message.py
Used to parsing message got from iGS01/iGS03 BLE Gateways.
For example:
```
bin/parse_message.py '$GPRP,F973D9D36662,E7DAE08E6FC3,-87,02010612FF590080BC330100FFFFFFFF000004000000'
{'advertisement': {'flags': 6,
 'localName': None,
 'manufacturerData': {'battery': 3.07,
 'code': 48256,
 'company': 'Ingics',
 'eventFlag': 0,
 'events': {'hall': false, 'boot': false},
 'mfg': 89,
 'raw': bytearray(b'Y\x00\x80\xbc3\x01\x00\xff\xff\xff\xff\x00\x00\x04\x00\x00'
                  b'\x00'),
 'type': 'iBS01H',
 'user': 0},
 'raw': bytearray(b'\x02\x01\x06\x12\xffY\x00\x80\xbc3\x01\x00\xff\xff\xff\xff'
                  b'\x00\x00\x04\x00\x00\x00'),
 'serviceData': [],
 'serviceSolicitationUuids': [],
 'serviceUuids': [],
 'txPowerLevel': None},
 'beacon': 'F973D9D36662',
 'fullMessage': '$GPRP,F973D9D36662,E7DAE08E6FC3,-87,02010612FF590080BC330100FFFFFFFF000004000000',
 'gateway': 'E7DAE08E6FC3',
 'rssi': -87,
 'timestamp': 1621496836.461955}
```

### Example Code

#### Parse iBS01/02/03/04/05/06 BLE beacon adv payload
```
from igsparser import PayloadParser

PayloadParser.parse('02010612FF0D0083BCD60000FFFFFFFFFFFF15000000')
```

#### Parse iGS01/02/03 BLE gateway message
```
from igsparser import MessageParser

def cb(data, index):
    import pprint
    pprint.pprint(vars(data))

 MessageParser.parse('$GPRP,A8F9F2190E7A,A99213AA86EF,-77,02010612FF0D0083BCD60000FFFFFFFFFFFF15000000', cb)
```

#### For Python 2.7.5

The package has been test on Python 2.7.17.
But I cannot guarantee it casue the support officially stopped January 1 2020.
