import context
from igsparser import PayloadParser


def test_ibs09r():
    payload = '0201061AFF2C0888BC470100AAAA74000000000000000000000042100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09R'
    assert msd.battery == 3.27
    assert msd.range == 116
    assert msd.events.detect is False
    payload = '0201061AFF2C0888BC470120AAAA74000000000000000000000042100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09R'
    assert msd.battery == 3.27
    assert msd.range == 116
    assert msd.events.detect is True


def test_ibs09ps():
    payload = '0201061AFF2C0888BC470120AAAA01000000000000000000000043100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PS'
    assert msd.battery == 3.27
    assert msd.counter == 1
    assert msd.events.detect is True
    payload = '0201061AFF2C0888BC470100AAAA00000000000000000000000043100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PS'
    assert msd.battery == 3.27
    assert msd.counter == 0
    assert msd.events.detect is False


def test_ibs09pir():
    payload = '0201061AFF2C0888BC470110AAAAFFFF0000000000000000000044100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PIR'
    assert msd.battery == 3.27
    assert msd.events.pir is True
    payload = '0201061AFF2C0888BCFA0000AAAAFFFF0000000000000000000044100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09PIR'
    assert msd.battery == 2.50
    assert msd.events.pir is False


def test_ibs09ir():
    payload = '0201061AFF2C0888BC390120AAAAD1000000060000000000000047080000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09IR'
    assert msd.battery == 3.13
    assert msd.counter == 209
    assert msd.events.ir is True
    assert msd.events.button is False
    payload = '0201061AFF2C0888BC390101AAAAD0000000040000000000000047080000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09IR'
    assert msd.battery == 3.13
    assert msd.counter == 208
    assert msd.events.ir is False
    assert msd.events.button is True


def test_ibs08t():
    payload = '0201061AFF2C0888BC4701010B0BA3010102000000000000000045100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 3.27
    assert msd.temperature == 28.27
    assert msd.humidity == 41.9
    assert msd.lux == 513
    assert msd.user == 0
    assert msd.events.button is True
    payload = '0201061AFF2C0888BC2001006E281300B907000000000000000045100000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 2.88
    assert msd.temperature == 103.5
    assert msd.humidity == 1.9
    assert msd.lux == 1977
    assert msd.user == 0
    assert msd.events.button is False
    payload = '0201061AFF2C0888BC330100870DF5019982000000000000000045020900'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08T'
    assert msd.battery == 3.07
    assert msd.temperature == 34.63
    assert msd.humidity == 50.1
    assert msd.lux == 33433
    assert msd.user == 0
    assert msd.events.button is False


def test_ibs08tp():
    # Battery 3.27V, button pressed, int temp 25.00C, ext temp 75.00C, user=18
    payload = '0201061AFF2C0888BC470101C4094C1D0000000000000000120049000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08TP'
    assert msd.battery == 3.27
    assert msd.temperature == 25.00
    assert msd.temperatureExt == 75.00
    assert msd.user == 18
    assert msd.events.button is True
    # Battery 3.00V, no event, int temp -5.00C, ext temp -20.00C, user=200
    payload = '0201061AFF2C0888BC2C01000CFE30F80000000000000000140049000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08TP'
    assert msd.battery == 3.00
    assert msd.temperature == -5.00
    assert msd.temperatureExt == -20.00
    assert msd.user == 20
    assert msd.events.button is False


def test_ibs08p():
    # Battery 3.00V, no event, int temp -5.00C, ext temp -20.00C, user=200
    payload = '0201061AFF2C0888BC2C01000CFE30F80000000000000000C8004B000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08P'
    assert msd.battery == 3.00
    assert msd.temperature == -5.00
    assert msd.temperatureExt == -20.00
    assert msd.user == 200
    assert msd.events.button is False
    # Battery 3.27V, button, int temp 25.00C, ext temp 75.00C, user=18
    payload = '0201061AFF2C0888BC470101C4094C1D000000000000000012004B000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08P'
    assert msd.battery == 3.27
    assert msd.temperature == 25.00
    assert msd.temperatureExt == 75.00
    assert msd.user == 18
    assert msd.events.button is True


def test_ibs08ad_ntc():
    # Battery 3.20V, button, NTC temp 45.67C, user=50
    payload = '0201061AFF2C0888BC4001010000D711000000000000000032004A000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-NTC'
    assert msd.battery == 3.20
    assert msd.temperatureExt == 45.67
    assert msd.user == 50
    assert msd.events.button is True
    # Battery 3.10V, no button, NTC temp 100.00C, user=0
    payload = '0201061AFF2C0888BC36010000001027000000000000000000004A000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-NTC'
    assert msd.battery == 3.10
    assert msd.temperatureExt == 100.00
    assert msd.user == 0
    assert msd.events.button is False


def test_ibs08ad_v():
    # Battery 3.10V, button, voltage 3300mV, user=171
    payload = '0201061AFF2C0888BC3601010000E40C0000000000000000AB0051000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-V'
    assert msd.battery == 3.10
    assert msd.voltage == 3300
    assert msd.user == 171
    assert msd.events.button is True
    # Battery 3.27V, no button, voltage 12000mV, user=0
    payload = '0201061AFF2C0888BC4701000000E02E0000000000000000000051000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-V'
    assert msd.battery == 3.27
    assert msd.voltage == 12000
    assert msd.user == 0
    assert msd.events.button is False


def test_ibs08ad_a():
    # Battery 3.30V, button, current 12000uA, user=153
    payload = '0201061AFF2C0888BC4A01010000E02E0000000000000000990053000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-A'
    assert msd.battery == 3.30
    assert msd.current == 12000
    assert msd.user == 153
    assert msd.events.button is True
    # Battery 3.00V, no button, current 4000uA, user=0
    payload = '0201061AFF2C0888BC2C01000000A00F0000000000000000000053000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-A'
    assert msd.battery == 3.00
    assert msd.current == 4000
    assert msd.user == 0
    assert msd.events.button is False


def test_ibs08ad_d():
    # Battery 3.20V, button+din, count 500, user=85
    payload = '0201061AFF2C0888BC4001410000F4010000000000000000550052000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-D'
    assert msd.battery == 3.20
    assert msd.counter == 500
    assert msd.user == 85
    assert msd.events.button is True
    assert msd.events.din is True
    # Battery 3.27V, no event, count 0, user=0
    payload = '0201061AFF2C0888BC470100000000000000000000000000000052000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08AD-D'
    assert msd.battery == 3.27
    assert msd.counter == 0
    assert msd.user == 0
    assert msd.events.button is False
    assert msd.events.din is False


def test_ibs08q():
    # Battery 3.27V, button+din, count 1000, user=119
    payload = '0201061AFF2C0888BC4701410000E803000000000000000077004E000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08Q'
    assert msd.battery == 3.27
    assert msd.counter == 1000
    assert msd.user == 119
    assert msd.events.button is True
    assert msd.events.din is True
    # Battery 3.00V, no event, count 0, user=0
    payload = '0201061AFF2C0888BC2C010000000000000000000000000000004E000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08Q'
    assert msd.battery == 3.00
    assert msd.counter == 0
    assert msd.user == 0
    assert msd.events.button is False
    assert msd.events.din is False


def test_ibs08f():
    # Battery 3.27V, button+fall+din, count 5, user=18
    payload = '0201061AFF2C0888BC47014900000500000000000000000012004D000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08F'
    assert msd.battery == 3.27
    assert msd.counter == 5
    assert msd.user == 18
    assert msd.events.button is True
    assert msd.events.fall is True
    assert msd.events.din is True
    # Battery 3.00V, no event, count 0, user=0
    payload = '0201061AFF2C0888BC2C010000000000000000000000000000004D000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08F'
    assert msd.battery == 3.00
    assert msd.counter == 0
    assert msd.user == 0
    assert msd.events.button is False
    assert msd.events.fall is False
    assert msd.events.din is False


def test_ibs08b():
    # Battery 3.27V, button, temp 20.00C, humidity 65.0%, pressure 1013.5hPa, user=51
    payload = '0201061AFF2C0888BC470101D0078A02972700000000000033004F000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08B'
    assert msd.battery == 3.27
    assert msd.temperature == 20.00
    assert msd.humidity == 65.0
    assert msd.pressure == 1013.5
    assert msd.user == 51
    assert msd.events.button is True
    # Battery 3.00V, no button, temp 0.00C, humidity 50.0%, pressure 900.0hPa, user=0
    payload = '0201061AFF2C0888BC2C010000000000D0B422000000000000004F000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS08B'
    assert msd.battery == 3.00
    assert msd.temperature == 0.00
    assert msd.humidity == 0.0
    assert msd.pressure == 4628.8
    assert msd.user == 0
    assert msd.events.button is False


def test_ibs09():
    # Battery 3.30V, button pressed, user=170
    payload = '0201061AFF2C0888BC4A0101000000000000000000000000AA00540000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09'
    assert msd.battery == 3.30
    assert msd.user == 170
    assert msd.events.button is True
    # Battery 3.30V, no button, user=0
    payload = '0201061AFF2C0888BC4A01000000000000000000000000000000540000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'iBS09'
    assert msd.battery == 3.30
    assert msd.user == 0
    assert msd.events.button is False


def test_deprecated_ibs09i():
    # Battery 3.27V, button pressed, user=85
    # subtype 0x4C is no longer supported (deprecated)
    payload = '0201061AFF2C0888BC47010100000000000000000000000055004C000000'
    msd = PayloadParser.parse(payload).manufacturerData
    assert msd.type == 'Unknown Tag'
