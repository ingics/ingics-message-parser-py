# ingics-message-parser-python

Message parser for Ingics BLE beacon and gateway.

## Uasge

### Install
```
python setup.py install
```

### Example

#### Beacon payload parser
```
Python 2.7.5 (default, Aug  7 2019, 00:51:29) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from igsparser import PayloadParser
>>> PayloadParser.parse('02010612FF0D0083BCD60000FFFFFFFFFFFF15000000')
{'mfgCode': 13, 'temperature': -1, 'mfg': 'Ingics', 'battery': 214, 'raw': '0D0083BCD60000FFFFFFFFFFFF15000000', 'user': 65535, 'type': 'iBS03T', 'events': {'button': 0}}
```

#### Gateway message parser
```
Python 2.7.5 (default, Aug  7 2019, 00:51:29) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from igsparser import MessageParser
>>> def cb(data, index):
...     print '#{0}: #{1}'.format(index, data)
... 
>>> MessageParser.parse('$GPRP,A8F9F2190E7A,A99213AA86EF,-77,02010612FF0D0083BCD60000FFFFFFFFFFFF15000000', cb)
000D
BC83
#0: #{'payload': '02010612FF0D0083BCD60000FFFFFFFFFFFF15000000', 'beacon': 'A8F9F2190E7A', 'parsedPayload': {'mfgCode': 13, 'temperature': -1, 'mfg': 'Ingics', 'battery': 214, 'raw': '0D0083BCD60000FFFFFFFFFFFF15000000', 'user': 65535, 'type': 'iBS03T', 'events': {'button': 0}}, 'rssi': -77, 'type': 'GPRP', 'gateway': 'A99213AA86EF'}
```

