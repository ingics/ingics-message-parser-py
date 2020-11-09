from igsparser import MessageParser

def test_ibs02ir():
    message = '$GPRP,0081F9889BF9,DB024BFC4863,-44,02010612FF0D0083BC200120AAAAFFFF000002070000,1604900604'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS02IR2'
        assert msd.battery == 2.88
        assert msd.events.ir == True
    MessageParser.parse(message, handler)

def test_ibs02pir():
    message = '$GPRP,607771FCD6FB,DB024BFC4863,-49,02010612FF0D0083BC4A0110AAAAFFFF000001140000,1604900518'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS02PIR2'
        assert msd.battery == 3.3
        assert msd.events.pir == True
    MessageParser.parse(message, handler)

def test_ibs02m2():
    message = '$GPRP,806FB0C7C148,F008D1798BA4,-44,02010612FF0D0083BC3E0140AAAAFFFF000004070000'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS02M2'
        assert msd.events.din == True
    MessageParser.parse(message, handler)
