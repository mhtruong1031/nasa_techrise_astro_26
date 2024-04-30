import time
import busio
import board

import adafruit_lidarlite
import adafruit_ltr390
import adafruit_tsl2591
import adafruit_gps

from time import sleep

def main() -> None:
    # Board Init
    i2c  = board.I2C(board.SCL, board.SDA)
    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

    # Variable Adjustments
    coll_int = 1.0  # Time interval between samples in seconds

    # Save Directories
    light_save_path = 'resources/light.csv'
    gps_save_path   = 'resources/gps.csv'
    
    # Data Labels
    light_measurements = ["UV", "Light", "UV Index", "Lux Ambience", "Infrared", "Visible"]

    # Component Initialization
    ltr     = adafruit_ltr390.LTR390(i2c)               # UV light sensor - ltr390
    tsl     = adafruit_tsl2591.TSL2591(i2c)             # IFR light sensor - tsl2591
    lidar1  = adafruit_lidarlite.LIDARLite(i2c, 0x6A)   # Garmin LiDaR
    lidar2  = adafruit_lidarlite.LIDARLite(i2c, 0x62) 
    gps     = adafruit_gps.GPS(uart, debug=False)       # GPS

    while True:
        print(get_light_readings(ltr, tsl, light_measurements))
        print(get_lidar_readings(lidar1))
        print(get_lidar_readings(lidar1))
    

def get_lidar_readings(sensor):
        return sensor.distance

def get_light_readings(ltr: adafruit_ltr390.LTR390, tsl: adafruit_tsl2591.TSL2591, measurements: list) -> dict:  
    # LTR
    uv       = ltr.uvs  # Raw UV Measurement
    light    = ltr.light  # Raw Ambient Light Measurement
    uvi      = ltr.uvi  # UV Index
    lux      = ltr.lux  # Lux Ambience
    ltr_data = [uv, light, uvi, lux]

    # TSL
    ifr      = tsl.infrared  # Infrared Light Level
    vis      = tsl.visible   # Visible Light Level
    tsl_data = [ifr, vis]

    collective_data = ltr_data + tsl_data

    sample = {key:value for (key, value) in zip(measurements, collective_data)}
    return sample

def get_gps_readings(gps: adafruit_gps.GPS):
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    
    while True:
        if gps.has_fix:
            print("=" * 40)  # Print a separator line.
            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,  # month!
                    gps.timestamp_utc.tm_sec,
                )
            )
            print("Latitude: {0:.6f} degrees".format(gps.latitude))
            print("Longitude: {0:.6f} degrees".format(gps.longitude))
            print(
                "Precise Latitude: {} degs, {:2.4f} mins".format(
                    gps.latitude_degrees, gps.latitude_minutes
                )
            )
            print(
                "Precise Longitude: {} degs, {:2.4f} mins".format(
                    gps.longitude_degrees, gps.longitude_minutes
                )
            )
            print("Fix quality: {}".format(gps.fix_quality))

            if gps.satellites is not None:
                print("# satellites: {}".format(gps.satellites))
            if gps.altitude_m is not None:
                print("Altitude: {} meters".format(gps.altitude_m))
            if gps.speed_knots is not None:
                print("Speed: {} knots".format(gps.speed_knots))
            if gps.track_angle_deg is not None:
                print("Track angle: {} degrees".format(gps.track_angle_deg))
            if gps.horizontal_dilution is not None:
                print("Horizontal dilution: {}".format(gps.horizontal_dilution))
            if gps.height_geoid is not None:
                print("Height geoid: {} meters".format(gps.height_geoid))
        
             

if __name__ == '__main__':
    main()