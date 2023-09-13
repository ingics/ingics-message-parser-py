from igsparser import MessageParser

def test_iws01_deprecate():
    message = '$GPRP,EAC653D3AA8D,CCB97E7361A4,-44,02010612FF2C0883BC4A0100A10A3100000039000000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iWS01'
        assert msd.temperature == 27.21
        assert msd.humidity == 4.9
        assert msd.battery == 3.3
        assert msd.events.button is False
    MessageParser.parse(message, handler)

def test_iws01():
    message = '$GPRP,EAC653D3AA8D,CCB97E7361A4,-44,02010618FF2C0887BC4A0100A10A3100000000000000000039000000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iWS01'
        assert msd.temperature == 27.21
        assert msd.humidity == 4.9
        assert msd.battery == 3.3
        assert msd.events.button is False
    MessageParser.parse(message, handler)

