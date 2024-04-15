from igsparser import MessageParser, PayloadParser

def test_ibs08():
    message = '$GPRP,F83060BC466E,98F4AB891854,-82,02010612FF2C0883BC380120C0086608000048080400'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS08'
        assert msd.temperature == 21.5
        assert msd.temperatureEnv == 22.4
        assert msd.events.detect == True
    MessageParser.parse(message, handler)

def test_ibs08t():
    payload = '02010612FF2C0883BC4C0100CF080B02000041010C00'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 3.32
    assert msd.temperature == 22.55
    assert msd.humidity == 52.3
    assert msd.user == 0

def test_ibs08r():
    payload = '02010612FF2C0883BC280100AAAA7200000042090000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08R'
    assert msd.battery == 2.96
    assert msd.range == 114
    assert msd.user == 0

def test_ibs08ps():
    payload = '02010612FF2C0883BC1E012021071E00000043010100'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08PS'
    assert msd.battery == 2.86
    assert msd.value == 1825
    assert msd.counter == 30
    assert msd.user == 0
    payload = '02010612FF2C0883BC170100B2FF1800000043010100'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08PS'
    assert msd.battery == 2.79
    assert msd.value == -78
    assert msd.counter == 24
    assert msd.user == 0

def test_ibs08pir():
    payload = '02010612FF2C0883BC4A0110AAAAFFFF000044040000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08PIR'
    assert msd.battery == 3.3
    assert msd.events.pir == True
    assert msd.user == 0
