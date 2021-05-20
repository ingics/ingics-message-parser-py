from igsparser import PayloadParser


def test_windows_10_desktop():
    payload = '1EFF0600010920025E294E5E30809130E56E2CA4701DC8EBED5396B6320B8F'
    ad = PayloadParser.parse(payload)
    msd = ad.manufacturerData
    assert msd.company == 'Microsoft'
    assert msd.type == 'Windows 10 Desktop'
    assert msd.slat == '5E294E5E'


def test_apple_ibeacon():
    payload = '0201061AFF4C000215B9A5D27D56CC4E3AAB511F2153BCB96700010359D6'
    ad = PayloadParser.parse(payload)
    msd = ad.manufacturerData
    assert msd.company == 'Apple, Inc.'
    assert msd.uuid == 'B9A5D27D-56CC-4E3A-AB51-1F2153BCB967'
    assert msd.major == 1
    assert msd.minor == 857
    assert msd.tx == -42
