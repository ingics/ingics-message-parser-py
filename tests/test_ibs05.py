from igsparser import MessageParser


def test_ibs05():
    message = '$GPRP,EAC653D3AA8E,CCB97E7361A4,-44,02010612FF2C0883BC290101AAAAFFFF000030000000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS05'
        assert msd.events.button is True
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
        assert msd.events.moving is True
    MessageParser.parse(message, handler)


def test_ibs05co2():
    message = '$GPRP,C8B629D6DAC3,F008D1789294,-35,02010612FF2C0883BC270100AAAA6804000034010000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS05CO2'
        assert msd.co2 == 1128
        assert not hasattr(msd, 'temperature')
    MessageParser.parse(message, handler)


def test_ibs05rg():
    message = '$GPRP,806FB0C9963F,C3674946C293,-71,0201061BFF2C0886BC3E110A00F4FF00FF1600F6FF00FF1400F6FF08FF1704,1586245829'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS05RG'
        assert msd.battery == 3.18
        assert msd.events.moving is True
        assert msd.events.boot is True
        assert msd.accels[0].x == 10
        assert msd.accels[1].y == -10
        assert msd.accels[2].z == -248
    MessageParser.parse(message, handler)


def test_iws01():
    message = '$GPRP,EAC653D3AA8D,CCB97E7361A4,-44,02010612FF2C0883BC4A0100A10A3100000039000000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iWS01'
        assert msd.temperature == 27.21
        assert msd.humidity == 4.9
        assert msd.battery == 3.3
        assert msd.events.button is False
    MessageParser.parse(message, handler)
