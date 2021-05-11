from igsparser import MessageParser

def test_ibs05():
    message = '$GPRP,EAC653D3AA8E,CCB97E7361A4,-44,02010612FF2C0883BC290101AAAAFFFF000030000000'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS05'
        assert msd.events.button == True
    MessageParser.parse(message, handler)

def test_ibs05t():
    message = '$GPRP,EAC653D3AA8D,CCB97E7361A4,-44,02010612FF2C0883BC4A0100A10AFFFF000032000000'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS05T'
        assert msd.battery == 3.3
        assert msd.temperature == 27.21
    MessageParser.parse(message, handler)

def test_ibs05g():
    message = '$GPRP,EAC653D3AA8C,CCB97E7361A4,-44,02010612FF2C0883BC290102AAAAFFFF000033000000'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS05G'
        assert msd.events.moving == True
    MessageParser.parse(message, handler)
