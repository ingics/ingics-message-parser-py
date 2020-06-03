from igsparser import PayloadParser

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
