from igsparser import MessageParser

def test_ibs06():
    message = '$GPRP,1804ED7048F5,E3C33FF55AEC,-55,02010612FF2C0883BC4A0100AAAAFFFF000040110000'
    def handler(data, index):
        assert data.beacon == '1804ED7048F5'
        assert data.gateway == 'E3C33FF55AEC'
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS06'
        assert msd.battery == 3.3
    MessageParser.parse(message, handler)
