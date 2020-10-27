from bluepy.btle import Scanner, DefaultDelegate
import binascii
from igsparser import MsdParser
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
            value = dev.getValueText(255)
            if value:
                if type(value) is not str:
                    # for python2, convert unicode to str
                    value = value.encode('ascii', 'ignore')
                data = MsdParser.parse(value)
                pprint.pprint(vars(data))

scanner = Scanner().withDelegate(ScanDelegate())
scanner.start()
while True:
    scanner.process()
