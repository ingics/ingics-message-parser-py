from bluepy.btle import Scanner, DefaultDelegate
import binascii
from igsparser import PayloadParser
import pprint

# MACs of IBSXX devices
ibs = [
        'F9:73:D9:D3:66:62',
        '60:77:71:FC:D6:DB'
]

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr.upper() in ibs:
            payload = binascii.b2a_hex(dev.rawData).decode('ascii')
            data = PayloadParser.parse(payload).manufacturerData
            pprint.pprint(vars(data))

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(100.0, passive=True)
