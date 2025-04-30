import context
from igsparser import MessageParser


def test_ibs04():
    message = '$GPRP,1804ED7048F5,E3C33FF55AEC,-55,02010612FF0D0083BC3A0101AAAAFFFF000019070000'

    def handler(data, index):
        assert data.beacon == '1804ED7048F5'
        assert data.gateway == 'E3C33FF55AEC'
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS04'
        assert msd.battery == 3.14
        assert msd.events.button is True
    MessageParser.parse(message, handler)
