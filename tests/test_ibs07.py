import context
from igsparser import MessageParser


def test_ibs07():
    message = '$GPRP,C7B3D4AE866D,F008D1789200,-57,02010618FF2C0887BC330100110B31005A002AFF02007B0050070000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS07'
        assert msd.battery == 3.07
        assert msd.temperature == 28.33
        assert msd.humidity == 49
        assert msd.lux == 90
        assert msd.accel.x == -214
        assert msd.accel.y == 2
        assert msd.accel.z == 123
        assert msd.events.button is False
    MessageParser.parse(message, handler)


def test_ibs07_no_sensor():
    message = '$GPRP,C7B3D4AE866D,F008D1789200,-57,02010618FF2C0887BC330101AAAAFFFF00002AFF02007B0050070000'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS07'
        assert msd.battery == 3.07
        assert not hasattr(msd, 'temperature')
        assert not hasattr(msd, 'humidity')
        assert not hasattr(msd, 'lux')
        assert msd.accel.x == -214
        assert msd.accel.y == 2
        assert msd.accel.z == 123
        assert msd.events.button is True
    MessageParser.parse(message, handler)
