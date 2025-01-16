import json
from igsparser import MessageParser, PayloadParser


def test_old_ibs01_button_pressed():
    message = '$GPRP,FE581D9DB308,2F9203AFA66B,-21,02010612FF590080BC360101FFFFFFFFFFFFFFFFFFFF'

    def handler(data, index):
        assert data.beacon == 'FE581D9DB308'
        assert data.gateway == '2F9203AFA66B'
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS01'
        assert msd.battery == 3.10
        assert msd.events.button is True
    MessageParser.parse(message, handler)


def test_old_ibs01_hall_detected():
    message = '$GPRP,F704B6D48BE8,1173AE7325A2,-24,02010612FF590080BC2B0104FFFFFFFFFFFFFFFFFFFF'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS01'
        assert msd.battery == 2.99
        assert msd.events.hall is True
    MessageParser.parse(message, handler)


def test_old_ibs01_moving_and_fall():
    payload = '02010612FF590080BC2B010AFFFFFFFFFFFFFFFFFFFF'
    ad = PayloadParser.parse(payload)
    msd = ad.manufacturerData
    assert msd.events.fall is True
    assert msd.events.moving is True


def test_old_ibs01_json_temperature():
    message = '{"data":["$GPRP,7ABA6F20ACCF,806172C89C09,-2,02010612FF590080BCFF00007A0D4300FFFFFFFFFFFF"]}'

    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.humidity == 67
        assert msd.temperature == 34.50
    MessageParser.parse(message, handler)


def test_ibs01t():
    messages = { 'data': [
        '$GPRP,C874A59968B3,F008D1789208,-59,02010612FF590080BC2E0100BF0A3900000005000000',
        '$GPRP,FB45C77FD45B,F008D1789200,-29,02010612FF590080BC1801017FF84300000005000000',
        '$GPRP,FB45C77FD45B,F008D1789200,-30,02010612FF590080BC1A01001027FFFF000007000000'
    ]}
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS01T'
        if index == 0:
            assert msd.humidity == 57
            assert msd.temperature == 27.51
            assert msd.events.button is False
        elif index == 1:
            assert msd.battery == 2.8
            assert msd.humidity == 67
            assert msd.temperature == -19.21
            assert msd.events.button is True
        elif index == 2:
            assert msd.battery == 2.82
            assert hasattr(msd, 'humidity') is False
            assert msd.temperature == 100.0
            assert msd.events.button is False
    MessageParser.parse(json.dumps(messages), handler)    

def test_ibs01h():
    messages = { 'data': [
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC160100FFFF0000000004030000',
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC160101FFFF0000000004030000',
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC160104FFFF0000000004030000',
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC160105FFFF0000000004030000',
    ]}
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS01H'
        assert msd.battery == 2.78
        if index == 0:
            assert msd.events.button is False
            assert msd.events.hall is False
        elif index == 1:
            assert msd.events.button is True
            assert msd.events.hall is False
        elif index == 2:
            assert msd.events.button is False
            assert msd.events.hall is True
        elif index == 3:
            assert msd.events.button is True
            assert msd.events.hall is True
    MessageParser.parse(json.dumps(messages), handler)    

def test_ibs01g():
    messages = { 'data': [
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC3A0100FFFF0000000006030000',
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC3A0101FFFF0000000006030000',
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC3A0102FFFF0000000006030000',
        '$GPRP,E856715A54F5,F008D1789200,-60,02010612FF590080BC3A0108FFFF0000000006030000',
    ]}
    def handler(data, index):
        msd = data.advertisement.manufacturerData
        assert msd.type == 'iBS01G'
        assert msd.battery == 3.14
        if index == 0:
            assert msd.events.button is False
            assert msd.events.moving is False
            assert msd.events.fall is False
        elif index == 1:
            assert msd.events.button is True
            assert msd.events.moving is False
            assert msd.events.fall is False
        elif index == 2:
            assert msd.events.button is False
            assert msd.events.moving is True
            assert msd.events.fall is False
        elif index == 3:
            assert msd.events.button is False
            assert msd.events.moving is False
            assert msd.events.fall is True
    MessageParser.parse(json.dumps(messages), handler)
