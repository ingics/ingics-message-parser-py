from igsparser import MessageParser, PayloadParser


def test_ibs03t():
    message = '$GPRP,0C61CFC14A4E,E3C33FF55AEC,-50,02010612FF0D0083BC2801020A09FFFF000015030000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03T'
        assert msd.temperature == 23.14
        assert msd.events.button is False
        assert not hasattr(msd, 'humidity')
    MessageParser.parse(message, handler)


def test_ibs03g():
    payload = '02010612FF0D0083BC3E0102AAAAFFFF000016130000'
    adv = PayloadParser.parse(payload)
    msd = adv.manufacturerData
    assert msd.type == 'iBS03G'
    assert msd.events.moving is True


def test_ibs03t_rh():
    message = '$GPRP,0081F96B8F51,98F4AB891854,-66,02010612FF0D0083BC3E0100AA073100000014130000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03T'
        assert msd.temperature == 19.62
        assert msd.humidity == 49
    MessageParser.parse(message, handler)


def test_ibs03rg():
    message = '$GPRP,806FB0C9963F,C3674946C293,-71,02010619FF0D0081BC3E110A00F4FF00FF1600F6FF00FF1400F6FF08FF,1586245829'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03RG'
        assert msd.battery == 3.18
        assert msd.events.moving is True
        assert msd.accels[0].x == 10
        assert msd.accels[1].y == -10
        assert msd.accels[2].z == -248
    MessageParser.parse(message, handler)


def test_ibs03tp():
    message = '$GPRP,1804ED7D9C00,C82B96AE3B04,-48,02010612FF0D0083BC280100D809060A640017040000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.company == 'Ingics'
        assert msd.type == 'iBS03TP'
        assert msd.battery == 2.96
        assert msd.temperature == 25.20
        assert msd.temperatureExt == 25.66
    MessageParser.parse(message, handler)


def test_ibs03r():
    message = '$GPRP,0C61CFC14A4E,E3C33FF55AEC,-50,02010612FF0D0083BC280100AAAA7200000013090000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03R'
        assert msd.range == 114
        assert not hasattr(msd, 'humidity')
    MessageParser.parse(message, handler)


def test_ibs03p():
    message = '$GPRP,0C61CFC14745,E7DAE08E6FC3,-67,02010612FF0D0083BC280100AAAAD207000012080000,1608516227'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03P'
        assert msd.temperatureExt == 20.02
        assert not hasattr(msd, 'humidity')
    MessageParser.parse(message, handler)


def test_ibs03gp():
    message = '$GPRP,806FB0C9963F,C3674946C293,-71,0201061BFF0D0085BC3111160082FF9EFE4E001200D2FE10003A005CFFD9C5'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03GP'
        assert msd.battery == 3.05
        assert msd.events.moving is True
        assert msd.accels[0].x == 22
        assert msd.accels[1].y == 18
        assert msd.accels[2].z == -164
        assert msd.gp == 1012.98
    MessageParser.parse(message, handler)



def test_ibs03rs():
    message = '$GPRP,F88A5EB8F226,F008D1798C68,-62,02010612FF0D0083BC430100AAAA150000001A040600'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03RS'
        assert msd.range == 21
        assert msd.battery == 3.23
    MessageParser.parse(message, handler)

def test_ibs03f():
    message = '$GPRP,70B9507273F0,F008D1789200,-65,02010612FF0D0083BC290140AAAA000000001B090000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03F'
        assert msd.events.din is True
    MessageParser.parse(message, handler)

def test_ibs03q():
    message = '$GPRP,70B9507273F0,F008D1789200,-65,02010612FF0D0083BC330140AAAA030000001C090000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03Q'
        assert msd.battery == 3.07
        assert msd.counter == 3
        assert msd.events.din is True
    MessageParser.parse(message, handler)

def test_ibs03qy():
    message1 = '$GPRP,70B9507273F0,F008D1789200,-65,02010612FF0D0083BC290148AAAA050000001D090000'

    def handler1(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03QY'
        assert msd.battery == 2.97
        assert msd.counter == 5
        assert msd.events.din is True
        assert msd.events.din2 is True
    MessageParser.parse(message1, handler1)

    message2 = '$GPRP,70B9507273F0,F008D1789200,-65,02010612FF0D0083BC290108AAAAFF0000001D090000'

    def handler2(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03QY'
        assert msd.battery == 2.97
        assert msd.counter == 255
        assert msd.events.din is False
        assert msd.events.din2 is True
    MessageParser.parse(message2, handler2)

def test_ibs03ad_ntc():
    message = '$GPRP,1804ED7D9C00,C82B96AE3B04,-48,02010612FF0D0083BC280100D809060A640023040000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03AD-NTC'
        assert msd.battery == 2.96
        assert hasattr(msd, 'temperature') == False
        assert msd.temperatureExt == 25.66
        assert msd.user == 100
    MessageParser.parse(message, handler)

def test_ibs03ad_v():
    message = '$GPRP,1804ED7D9C00,C82B96AE3B04,-48,02010612FF0D0083BC280100D809060A640024040000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03AD-V'
        assert msd.battery == 2.96
        assert hasattr(msd, 'temperature') == False
        assert msd.voltage == 2566
        assert msd.user == 100
    MessageParser.parse(message, handler)

def test_ibs03ad_d():
    message = '$GPRP,1804ED7D9C00,C82B96AE3B04,-48,02010612FF0D0083BC280140D809060A640025040000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03AD-D'
        assert msd.battery == 2.96
        assert hasattr(msd, 'temperature') == False
        assert msd.events.din is True
        assert msd.user == 100
        assert msd.counter == 2566
    MessageParser.parse(message, handler)

def test_ibs03ad_a():
    message = '$GPRP,1804ED7D9C00,C82B96AE3B04,-48,02010612FF0D0083BC280140D809060A640026040000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03AD-A'
        assert msd.battery == 2.96
        assert msd.current == 2566
        assert msd.user == 100
        assert hasattr(msd, 'temperature') == False
    MessageParser.parse(message, handler)
