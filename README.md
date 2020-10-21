# ingics-message-parser-py

Message parser for Ingics BLE beacon and gateway.


## Uasge

### Install

```
pip install -U git+https://github.com/ingics/ingics-message-parser-py
```

### Unit Test
```
PYTHONPATH=. pytest -v
```

### Example

#### Beacon payload parser
```
Python 3.6.9 (default, Apr 18 2020, 01:56:04)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from igsparser import PayloadParser
>>> PayloadParser.parse('02010612FF0D0083BCD60000FFFFFFFFFFFF15000000')
{'flags': 6,
 'localName': None,
 'manufacturerData': {'battery': 2.14,
 'code': 48259,
 'company': 'Ingics',
 'eventFlag': 0,
 'events': {'button': 0},
 'mfg': 13,
 'raw': bytearray(b'\r\x00\x83\xbc\xd6\x00\x00\xff\xff\xff\xff\xff'
                  b'\xff\x15\x00\x00\x00'),
 'temperature': -0.01,
 'type': 'iBS03T',
 'user': 65535},
 'raw': bytearray(b'\x02\x01\x06\x12\xff\r\x00\x83\xbc\xd6\x00\x00'
                  b'\xff\xff\xff\xff\xff\xff\x15\x00\x00\x00'),
 'serviceData': [],
 'serviceSolicitationUuids': [],
 'serviceUuids': [],
 'txPowerLevel': None}
```

#### Gateway message parser
```
Python 3.8.0 (default, Oct 15 2019, 22:57:01)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from igsparser import MessageParser
>>> def cb(data, index):
...     import pprint
...     pprint.pprint(vars(data))
...
>>> MessageParser.parse('$GPRP,A8F9F2190E7A,A99213AA86EF,-77,02010612FF0D0083BCD60000FFFFFFFFFFFF15000000', cb)
{'advertisement': {'flags': 6,
 'localName': None,
 'manufacturerData': {'battery': 2.14,
 'code': 48259,
 'company': 'Ingics',
 'eventFlag': 0,
 'events': {'button': 0},
 'mfg': 13,
 'raw': bytearray(b'\r\x00\x83\xbc\xd6\x00\x00\xff\xff\xff\xff\xff'
                  b'\xff\x15\x00\x00\x00'),
 'temperature': -0.01,
 'type': 'iBS03T',
 'user': 65535},
 'raw': bytearray(b'\x02\x01\x06\x12\xff\r\x00\x83\xbc\xd6\x00\x00'
                  b'\xff\xff\xff\xff\xff\xff\x15\x00\x00\x00'),
 'serviceData': [],
 'serviceSolicitationUuids': [],
 'serviceUuids': [],
 'txPowerLevel': None},
 'beacon': 'A8F9F2190E7A',
 'fullMessage': '$GPRP,A8F9F2190E7A,A99213AA86EF,-77,02010612FF0D0083BCD60000FFFFFFFFFFFF15000000',
 'gateway': 'A99213AA86EF',
 'rssi': -77,
 'timestamp': 1591154801.380887}
```

#### For Python 2.7.5
Current package is useable on Python 2.7.5, too.
```
Python 2.7.17 (default, Apr 15 2020, 17:20:14)
[GCC 7.5.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from igsparser import MessageParser
>>> def cb(data, index):
...     import pprint
...     pprint.pprint(vars(data))
...
>>> MessageParser.parse('$GPRP,A8F9F2190E7A,A99213AA86EF,-77,02010612FF0D0083BCD60000FFFFFFFFFFFF15000000', cb)
{'advertisement': {'flags': 6,
 'localName': None,
 'manufacturerData': {'battery': 2,
 'code': 48259,
 'company': 'Ingics',
 'eventFlag': 0,
 'events': {'button': 0},
 'mfg': 13,
 'raw': bytearray(b'\r\x00\x83\xbc\xd6\x00\x00\xff\xff\xff\xff\xff\xff\x15\x00\x00\x00'),
 'temperature': -1,
 'type': 'iBS03T',
 'user': 65535},
 'raw': bytearray(b'\x02\x01\x06\x12\xff\r\x00\x83\xbc\xd6\x00\x00\xff\xff\xff\xff\xff\xff\x15\x00\x00\x00'),
 'serviceData': [],
 'serviceSolicitationUuids': [],
 'serviceUuids': [],
 'txPowerLevel': None},
 'beacon': 'A8F9F2190E7A',
 'fullMessage': '$GPRP,A8F9F2190E7A,A99213AA86EF,-77,02010612FF0D0083BCD60000FFFFFFFFFFFF15000000',
 'gateway': 'A99213AA86EF',
 'rssi': -77,
 'timestamp': 1591162157.305131}
```
