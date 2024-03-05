import board
import adafruit_ltr390
import adafruit_tsl2591
import adafruit_gps

from csv import DictWriter
from threading import Thread
from time import sleep

def main() -> None:
    # I2C Init
    i2c = board.I2C(board.SCL, board.SDA)

    # Variable Adjustments
    batch_size     = 20
    light_coll_int = 1.0  # Time interval between samples in seconds
    gps_coll_int   = 1.0  # Time interval between samples in seconds

    # Save Directories
    light_save_path = 'resources/light.csv'
    gps_save_path   = 'resources/gps.csv'
    
    # Component Initialization
    ltr = adafruit_ltr390.LTR390(i2c)  # UV light sensor - ltr390
    tsl = adafruit_tsl2591.TSL2591(i2c)  # IFR light sensor - tsl2591
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # GPS

    # Threading for data collection with light, gps, LiDAR
    t_light = Thread(thread_light_readings, args=(ltr, tsl, batch_size, light_save_path, light_coll_int))
    t_gps   = Thread(thread_gps_readings, args=(gps, batch_size, gps_save_path, gps_coll_int))
    threads = [t_light, t_gps]

    for thread in threads:
        thread.daemon = True
        thread.start()


def thread_gps_readings(gps: adafruit_gps.GPS_GtopI2C, batch_size: int, save_path: str, time_int: int) -> None:
    measurements = ["Timestamp", "Lattitude", "Longitude"]
    batch        = []

    curr_batch = 0
    while True:
        if curr_batch < batch_size:  # Writing of data every batch_size samples
            sample = get_gps_readings(gps, measurements)
            batch.append(save_path, sample)
        else:
            write_to_csv(save_path, batch, measurements)
            batch = []
        sleep(time_int)


def thread_light_readings(ltr: adafruit_ltr390.LTR390, tsl: adafruit_tsl2591.TSL2591, batch_size: int, save_path: str, time_int: int) -> None:
    measurements = ["UV", "Light", "UV Index", "Lux Ambience", "Infrared", "Visible"]
    batch        = []

    curr_batch = 0
    while True:
        if curr_batch < batch_size:
            sample = get_light_readings(ltr, tsl, measurements)
            batch.append(sample)
        else:
            write_to_csv(save_path, batch, measurements)
            batch = []
        sleep(time_int)

# Returns the various GPS readings
def get_gps_readings(gps: adafruit_gps.GPS_GtopI2C, measurements: list) -> dict:
    if not gps.update(): 
        print("Waiting for fix...")

    timestamp = "{:02}{:02}{:02}".format(  # HH:MM:SS
        gps.timestamp_utc.tm_hour,
        gps.timestamp_utc.tm_min,
        gps.timestamp_utc.tm_sec
    )
    lattitude = gps.latitude
    longitude = gps.longitude
    collective_data = [timestamp, lattitude, longitude]

    sample = {key:value for (key, value) in zip(measurements, collective_data)}
    return sample

# Returns the various light readings from the LTR390
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

def write_to_csv(path: str, data: list, field_names: list) -> None:
    with open(path, 'a') as csvfile: 
        writer = DictWriter(csvfile, fieldnames = field_names) 
        writer.writeheader() 
        writer.writerows(data) 


if __name__ == '__main__':
    main()