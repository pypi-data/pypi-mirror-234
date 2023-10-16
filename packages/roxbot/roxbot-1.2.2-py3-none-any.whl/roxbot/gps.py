#!/usr/bin/env python3
"""
 gps convertors and utils

 Copyright (c) 2023 ROX Automation

fix types:
    0 = Invalid, no position available.
    1 = Autonomous GPS fix, no correction data used.
    2 = DGPS fix, using a local DGPS base station or correction service, such as WAAS.
    3 = PPS fix, never used?.
    4 = RTK fix, high accuracy Real Time Kinematic.
    5 = RTK Float, better than DGPS, but not quite RTK.
    6 = Estimated fix (dead reckoning).
    7 = Manual input mode.
    8 = Simulation mode.
    9 = WAAS fix (not NMEA standard, but NovAtel receivers report this instead of a 2).

"""
import asyncio
import logging
import operator
from collections import OrderedDict
from datetime import datetime
from functools import reduce
from typing import Optional, Tuple

import serial_asyncio  # type: ignore

from roxbot.interfaces import Pose
from roxbot.converters import enu_to_latlon, theta_to_heading


def sd_to_dm(latitude: float, longitude: float) -> Tuple[str, str, str, str]:
    """convert decimals to DDDMM.SSSS format and their directions"""

    if latitude < 0:
        lat_dir = "S"
    else:
        lat_dir = "N"
    lat = ("%010.5f" % (abs(int(latitude)) * 100 + (abs(latitude) % 1.0) * 60)).rstrip(
        "0"
    )

    if longitude < 0:
        lon_dir = "W"
    else:
        lon_dir = "E"
    lon = (
        "%011.5f" % (abs(int(longitude)) * 100 + (abs(longitude) % 1.0) * 60)
    ).rstrip("0")

    return lat, lat_dir, lon, lon_dir


def nmea_msg(sentence):
    """add starting $ and checksum to a message"""
    checksum = reduce(operator.xor, map(ord, sentence), 0)
    return "${}*{:02x}".format(sentence, checksum)


class NMEA_Message:
    """nmea message generator"""

    def __init__(self, sentence_type, fields: OrderedDict):
        self.sentence_type = sentence_type
        self.fields = fields

    def __str__(self):
        sentence = "{},{}".format(self.sentence_type, ",".join(self.fields.values()))
        return nmea_msg(sentence)

    def get(self, name: str) -> str:
        """get field value"""
        return self.fields[name]

    def set(self, name: str, val: str):
        """set field value"""
        self.fields[name] = val

    def timestamp_now(self):
        """set timestamp to current time"""
        self.set("timestamp", datetime.now().strftime("%H%M%S.%f")[:-3])


def message_factory(
    sentence_type: str, field_names: list, example_str: str
) -> NMEA_Message:
    """create a message class"""

    vals = [str(f) for f in example_str.split(",")]
    fields = OrderedDict(zip(field_names, vals))

    return NMEA_Message(sentence_type, fields)


def ssn_message() -> NMEA_Message:
    """
    see https://www.septentrio.com/system/files/support/asterx4_firmware_v4.10.0_reference_guide.pdf  # noqa

    $PSSN,HRP,142657.80,061222,152.236,,-0.708,0.084,,0.181,21,2,2.400,E*23

    """

    field_names = [
        "sentence_type",
        "timestamp",
        "date",
        "heading",
        "roll",
        "pitch",
        "heading_stdev",
        "roll_stdev",
        "pitch_stdev",
        "sats_used",
        "rtk_mode",
        "magnetic_variation",
        "mag_var_direction",
    ]

    example_str = "HRP,142657.80,061222,152.236,,-0.708,0.084,,0.181,21,2,2.400,E"

    return message_factory("PSSN", field_names, example_str)


def gga_message() -> NMEA_Message:
    """$GPGGA,115739.00,4158.8441367,N,09147.4416929,W,4,13,0.9,255.747,M,-32.00,M,01,0000*6E"""  # noqa

    field_names = [
        "timestamp",
        "lat",
        "NS",
        "lon",
        "EW",
        "fix_type",  # named gps_qual in pynmea2
        "nr_sattelites",
        "horizontal_dilution",
        "elevation",
        "M1",
        "geoid_height",
        "M2",
        "gps_age",
        "station_id",
    ]
    example_str = "130000.00,0000.3934834,N,00604.9127445,E,4,20,0.7,23.1169,M,47.3944,M,3.2,0000"  # noqa

    return message_factory("GPGGA", field_names, example_str)


class Mock_GPS:
    """dummy gps, generates gps messages from pose,
    generates invalid fix now and then"""

    def __init__(
        self,
        nmea_out: Optional[str] = None,
        baudrate: int = 115200,
        n_valid: int = 100,
        n_invalid: int = 0,
    ) -> None:
        """n_valid: number of valid fixes before invalid fix,
        n_invalid: number of invalid fixes before valid fix"""

        self._log = logging.getLogger(self.__class__.__name__)

        self._nmea_out = nmea_out
        self._baudrate = baudrate

        # pose in enu coordinates (x,y,theta)
        self._pose = Pose()

        self._gga = gga_message()
        self._ssn = ssn_message()

        # fix quality list
        self._fix_qual = [4] * n_valid + [0] * n_invalid
        self._fix_counter = 0  # update on gga message

    def set_pose(self, x, y, theta):
        """set pose"""
        self._pose = Pose(x, y, theta)

    def nmea_gga(self, latlon: Tuple[float, float]) -> str:
        """generate gga message (position)"""

        self._gga.timestamp_now()
        for k, v in zip(("lat", "NS", "lon", "EW"), sd_to_dm(*latlon)):
            self._gga.set(k, v)

        # update fix quality
        self._gga.set("fix_type", str(self._fix_qual[self._fix_counter]))
        self._fix_counter = (self._fix_counter + 1) % len(self._fix_qual)

        return str(self._gga)

    def nmea_ssn(self, heading: float) -> str:
        """generate ssn message (heading)"""

        self._ssn.timestamp_now()
        self._ssn.set("heading", "{:.3f}".format(heading))

        return str(self._ssn)

    async def main(self, freq: float = 1.0):
        """main loop, generate gps messages and publish to serial port"""
        delay = 1 / freq

        if self._nmea_out is None:
            writer = None
        else:
            _, writer = await serial_asyncio.open_serial_connection(
                url=self._nmea_out, baudrate=self._baudrate
            )

        while True:
            self._log.debug("%s", f"pose: {self._pose}")

            lat, lon = enu_to_latlon(self._pose.xy)

            gga_txt = self.nmea_gga((lat, lon))

            heading = theta_to_heading(self._pose.theta)

            self._log.debug(
                "%s", f"lat: {lat:.8f}, lon: {lon:.8f}, heading: {heading:.3f}"
            )
            ssn_txt = self.nmea_ssn(heading)

            self._log.debug("%s", f"{gga_txt=}")
            self._log.debug("%s", f"{ssn_txt=}")

            if writer is not None:
                writer.write((gga_txt + "\r\n").encode("ascii"))
                writer.write((ssn_txt + "\r\n").encode("ascii"))

            await asyncio.sleep(delay)


def demo():
    """demo gps messages"""

    gps = Mock_GPS()

    print("Sending messages, press Ctrl-C to stop")
    try:
        asyncio.run(gps.main(1))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    import coloredlogs  # type: ignore

    coloredlogs.install(
        level="DEBUG", fmt="%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s"
    )
    demo()
