from igsparser import MessageParser


def test_ibs06():
    message = '$GPRP,1804ED7048F5,E3C33FF55AEC,-55,02010612FF2C0883BC4A0100AAAAFFFF000040110000'

    def handler(data, index):
        assert data.beacon == '1804ED7048F5'
        assert data.gateway == 'E3C33FF55AEC'
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS06'
        assert msd.battery == 3.3
        assert hasattr(msd.events, 'button') is False
    MessageParser.parse(message, handler)


def test_ibs06i():
    message = '$RSPR,EB8C79A8F138,F008D1789200,-89,12FF2C0883BC350100AAAAFFFF000036030000,1639557006.811'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS06i'
        assert msd.battery == 3.09
        assert hasattr(msd.events, 'button') is False
    MessageParser.parse(message, handler)
