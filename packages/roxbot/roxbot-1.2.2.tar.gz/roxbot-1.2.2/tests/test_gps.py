import os
from math import degrees, radians

import pynmea2
from pytest import approx
from roxbot import gps

# set reference point
os.environ["GPS_REF"] = "51.0,6.0"


from roxbot import converters  # pylint: disable=wrong-import-position


def test_angle_conversion():
    """test heading and theta conversions, using enu coordinates"""
    T = [0, 90, -10, -80, 170]

    H = [90, 0, 100, 170, -80]
    for heading, theta in zip(H, T):
        assert heading == approx(converters.theta_to_heading(radians(theta)))

        assert theta == approx(degrees(converters.heading_to_theta(heading)))


def test_directions():
    lat = 51.0
    lon = 6.0

    converters.GPS_REF = (lat, lon)

    xy = (10, 10)
    lat2, lon2 = converters.enu_to_latlon(xy)

    assert lat2 > lat
    assert lon2 > lon

    x, y = converters.latlon_to_enu((lat, lon))
    assert x == 0
    assert y == 0


def test_ssn():
    """test SSN message generation"""

    target = "$PSSN,HRP,142657.80,061222,152.236,,-0.708,0.084,,0.181,21,2,2.400,E*23"

    msg = gps.ssn_message()

    assert target == str(msg)

    heading = msg.get("heading")
    assert heading == "152.236"

    assert msg.get("heading_stdev") == "0.084"

    # set value
    msg.set("heading", "foo")

    sentence = "PSSN,HRP,142657.80,061222,foo,,-0.708,0.084,,0.181,21,2,2.400,E"

    assert str(msg) == gps.nmea_msg(sentence)


def test_conversion():
    out = gps.sd_to_dm(-19.484083333333334, 24.1751)
    assert out == ("1929.045", "S", "02410.506", "E")

    out = gps.sd_to_dm(19.484083333333334, -24.1751)
    assert out == ("1929.045", "N", "02410.506", "W")


def test_gga():
    txt = "$GPGGA,142658.20,5127.3934834,N,00604.9127445,E,4,20,0.7,23.1169,M,47.3944,M,3.2,0000*73"  # noqa

    # use pynmea as reference
    msg = pynmea2.parse(txt)
    latitude = msg.latitude
    longitude = msg.longitude

    # own code
    msg = gps.gga_message()

    lat, ns, lon, ew = gps.sd_to_dm(latitude, longitude)
    msg.set("lat", lat)
    msg.set("lon", lon)
    msg.set("NS", ns)
    msg.set("EW", ew)

    # parse with nmea2
    msg = pynmea2.parse(txt)
    assert latitude == msg.latitude
    assert longitude == msg.longitude


def test_mock_gps():
    mock = gps.Mock_GPS()

    latlon = (51.365948, 6.172037)
    heading = 30.0

    gga_txt = mock.nmea_gga(latlon)
    msg = pynmea2.parse(gga_txt)
    assert msg.latitude == approx(latlon[0])
    assert msg.longitude == approx(latlon[1])

    _ = mock.nmea_ssn(heading)


def test_mock_fix():
    """check generation of invalid fix"""

    mock = gps.Mock_GPS(n_valid=90, n_invalid=10)

    latlon = (51.365948, 6.172037)

    qual = []

    for _ in range(200):
        gga_txt = mock.nmea_gga(latlon)
        msg = pynmea2.parse(gga_txt)
        qual.append(msg.gps_qual)

    assert all(q == 4 for q in qual[:90])
    assert all(q == 0 for q in qual[90:100])
    assert all(q == 4 for q in qual[100:190])
    assert all(q == 0 for q in qual[190:200])
