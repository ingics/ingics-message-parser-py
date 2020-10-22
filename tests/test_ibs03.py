from igsparser import MessageParser

def test_ibs03t():
    message = '$GPRP,0C61CFC14A4E,E3C33FF55AEC,-50,02010612FF0D0083BC2801020A09FFFF000015030000'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03T'
        assert msd.temperature == 23.14
        assert msd.events.button == False
        assert not hasattr(msd, 'humidity')
    MessageParser.parse(message, handler)

def test_ibs03t_new():
    message = '$GPRP,CDCB34E2D0A2,77AE1C1DC33D,-91,02010612FF0D0083BCAD0000A20B4700FFFF14000000'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03T'
        assert msd.temperature == 29.78
        assert msd.humidity == 71
    MessageParser.parse(message, handler)

def test_ibs03rg():
    message = '$GPRP,806FB0C9963F,C3674946C293,-71,02010619FF0D0081BC3E110A00F4FF00FF1600F6FF00FF1400F6FF08FF,1586245829'
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS03RG'
        assert msd.battery == 3.18
        assert msd.events.moving == True
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
