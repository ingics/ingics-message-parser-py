from igsparser import MessageParser

def test_ibs08():
    message = '$GPRP,F83060BC466E,98F4AB891854,-82,02010612FF2C0883BC380120C0086608000048080400'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS08'
        assert msd.temperature == 21.5
        assert msd.temperatureEnv == 22.4
        assert msd.events.detect == True
    MessageParser.parse(message, handler)
