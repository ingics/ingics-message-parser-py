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
    payload = '02010618FF2C0887BC2C01000B0BA301000000000000000041000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 3
    assert msd.temperature == 28.27
    assert msd.humidity == 41.9
    assert msd.events.button == False
    payload = '02010618FF2C0887BCE600016E281300000000000000000041000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 2.3
    assert msd.temperature == 103.5
    assert msd.humidity == 1.9
    assert msd.events.button == True

def test_ibs09r():
    payload = '02010618FF2C0887BC470100AAAA7400000000000000000042100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09R'
    assert msd.battery == 3.27
    assert msd.range == 116

def test_ibs09ps():
    payload = '02010618FF2C0887BC470120AAAA0100000000000000000043100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PS'
    assert msd.battery == 3.27
    assert msd.counter == 1
    assert msd.events.detect == True
    payload = '02010618FF2C0887BC470100AAAA0000000000000000000043100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PS'
    assert msd.battery == 3.27
    assert msd.counter == 0
    assert msd.events.detect == False

def test_ibs09pir():
    payload = '02010618FF2C0887BC470110AAAAFFFF000000000000000044100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PIR'
    assert msd.battery == 3.27
    assert msd.events.pir == True
    payload = '02010618FF2C0887BCFA0000AAAAFFFF000000000000000044100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PIR'
    assert msd.battery == 2.50
    assert msd.events.pir == False

def test_ibs09lx():
    payload = '02010618FF2C0887BC470101AAAAFFFF010200000000000045100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09LX'
    assert msd.battery == 3.27
    assert msd.lux == 513
    assert msd.events.button == True
    payload = '02010618FF2C0887BC200100AAAAFFFFB90700000000000045100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09LX'
    assert msd.battery == 2.88
    assert msd.lux == 1977
    assert msd.events.button == False

