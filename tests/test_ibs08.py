from igsparser import MessageParser, PayloadParser

def test_ibs09r():
    payload = '0201061AFF2C0888BC470100AAAA74000000000000000000000042100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09R'
    assert msd.battery == 3.27
    assert msd.range == 116
    assert msd.events.detect == False
    payload = '0201061AFF2C0888BC470120AAAA74000000000000000000000042100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09R'
    assert msd.battery == 3.27
    assert msd.range == 116
    assert msd.events.detect == True

def test_ibs09ps():
    payload = '0201061AFF2C0888BC470120AAAA01000000000000000000000043100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PS'
    assert msd.battery == 3.27
    assert msd.counter == 1
    assert msd.events.detect == True
    payload = '0201061AFF2C0888BC470100AAAA00000000000000000000000043100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PS'
    assert msd.battery == 3.27
    assert msd.counter == 0
    assert msd.events.detect == False

def test_ibs09pir():
    payload = '0201061AFF2C0888BC470110AAAAFFFF0000000000000000000044100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PIR'
    assert msd.battery == 3.27
    assert msd.events.pir == True
    payload = '0201061AFF2C0888BCFA0000AAAAFFFF0000000000000000000044100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PIR'
    assert msd.battery == 2.50
    assert msd.events.pir == False

def test_ibs08t():
    payload = '0201061AFF2C0888BC4701010B0BA3010102000000000000000045100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 3.27
    assert msd.temperature == 28.27
    assert msd.humidity == 41.9
    assert msd.lux == 513
    assert msd.events.button == True
    payload = '0201061AFF2C0888BC2001006E281300B907000000000000000045100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 2.88
    assert msd.temperature == 103.5
    assert msd.humidity == 1.9
    assert msd.lux == 1977
    assert msd.events.button == False
    payload = '0201061AFF2C0888BC330100870DF5019982000000000000000045020900'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 3.07
    assert msd.temperature == 34.63
    assert msd.humidity == 50.1
    assert msd.lux == 33433
    assert msd.events.button == False
