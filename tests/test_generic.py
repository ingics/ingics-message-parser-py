import context
from igsparser import PayloadParser, MessageParser


def test_localname():
    payload = '0B09506978656C203420584C'
    ad = PayloadParser.parse(payload)
    assert ad.localName == 'Pixel 4 XL'


def test_tx_power():
    payload = '0B09506978656C203420584C020AF5'
    ad = PayloadParser.parse(payload)
    assert ad.txPowerLevel == -11


def test_org_bluetooth_characteristic_temperature():
    payload = '0B09506978656C203420584C05166E2A1111'
    ad = PayloadParser.parse(payload)
    assert ad.serviceData[0]['uuid'] == 0x2A6E
    assert ad.temperature == 43.69
    assert ad.temperatureUnit == 'C'


def test_org_bluetooth_characteristic_humidity():
    payload = '0B09506978656C203420584C05166F2A1111'
    ad = PayloadParser.parse(payload)
    assert ad.serviceData[0]['uuid'] == 0x2A6F
    assert ad.humidity == 43.69


def test_16b_service_uuid():
    payload = '0B09506978656C203420584C0303011805166E2A1111'
    ad = PayloadParser.parse(payload)
    assert ad.serviceUuids[0] == '1801'


def test_128b_service_uuid():
    payload = '0B09506978656C203420584C1107A8A9DF2219FA62A00A471D2500615DE9'
    ad = PayloadParser.parse(payload)
    assert ad.serviceUuids[0] == 'E95D6100-251D-470A-A062-FA1922DFA9A8'


def test_appearance():
    payload = '031980000201060E094E6F726469635F426C696E6B79'
    ad = PayloadParser.parse(payload)
    assert ad.apperance == 'Generic Computer.'


def test_multi_messages():
    messages = [
        '$GPRP,7ABA6F20ACCF,806172C89C09,-2,02010612FF590080BCFF00007A0D4300FFFFFFFFFFFF',
        '$GPRP,F704B6D48BE8,1173AE7325A2,-24,02010612FF590080BC2B0104FFFFFFFFFFFFFFFFFFFF'
    ]
    data = MessageParser.parse('\n'.join(messages), None)
    index = 0
    while index < len(data):
        msd = data[index].advertisement.manufacturerData
        if index == 0:
            assert msd.humidity == 67
            assert msd.temperature == 34.50
        elif index == 1:
            assert msd.battery == 2.99
            assert msd.events.hall is True
        else:
            assert 'invalid index'
        index += 1


def test_multi_messages_cb():
    messages = [
        '$GPRP,7ABA6F20ACCF,806172C89C09,-2,02010612FF590080BCFF00007A0D4300FFFFFFFFFFFF',
        '$GPRP,F704B6D48BE8,1173AE7325A2,-24,02010612FF590080BC2B0104FFFFFFFFFFFFFFFFFFFF'
    ]

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        if index == 0:
            assert msd.humidity == 67
            assert msd.temperature == 34.50
        elif index == 1:
            assert msd.battery == 2.99
            assert msd.events.hall is True
        else:
            assert 'invalid index'
    MessageParser.parse('\n'.join(messages), handler)


def test_empty_payload():
    message = '$GPRP,7ABA6F20ACCF,806172C89C09,-2,'
    data = MessageParser.parse(message, None)
    ad = data[0].advertisement
    msd = ad.manufacturerData
    assert msd is None
    message = '$GPRP,7ABA6F20ACCF,806172C89C09,-2,,1575440728'
    data = MessageParser.parse(message, None)
    ad = data[0].advertisement
    msd = ad.manufacturerData
    assert msd is None
    assert data[0].timestamp == 1575440728
