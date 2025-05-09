import context
from igsparser import MessageParser


def test_ibs02hm():
    message = '$GPRP,F0F8F2CADCCF,C82B96AE3B04,-52,02010612FF0D0082BC280100AAAAFFFF000004050000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS02M2-RS'
        assert msd.battery == 2.96
    MessageParser.parse(message, handler)


def test_irs02rg():
    message = '$GPRP,0C61CFC14B58,CC4B73906F8C,-21,02010612FF0D0083BC4D010000002400FCFE22074B58,1575440728'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iRS02RG'
        assert msd.accel.x == 0
        assert msd.accel.z == -260
    MessageParser.parse(message, handler)
