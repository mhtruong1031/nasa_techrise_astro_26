# SPDX-FileCopyrightText: 2018 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Rangefinder byuit around the Garmin LidarLite

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2018 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""
import time
import busio
import board
import adafruit_lidarlite

i2c = busio.I2C(board.SCL, board.SDA)

sensor = adafruit_lidarlite.LIDARLite(i2c, address=0x6A)
sensor2 = adafruit_lidarlite.LIDARLite(i2c, address=0x62)

while True:
    try:
        print(sensor.distance, sensor2.distance, sep='\t')
        #print(sensor.distance)
    except RuntimeError as e:
        # If we get a reading error, just print it and keep truckin'
        print(e)
    time.sleep(0.5)
