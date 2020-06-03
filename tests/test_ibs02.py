from igsparser import MessageParser

def test_ibs02():
    message = '$GPRP,F0F8F2CADCCF,C82B96AE3B04,-52,02010612FF0D0082BC280100AAAAFFFF000004050000'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS02HM'
        assert msd.battery == 2.96
    MessageParser.parse(message, handler)
