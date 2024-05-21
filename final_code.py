import time
import sdcardio
import board
import busio
import digitalio
import storage
import astrobotic_lib
import adafruit_gps
import adafruit_lidarlite
import adafruit_ltr390
import adafruit_tsl2591

# Initialize flags
I2C_avail = False
I2C1_avail = False
I2C2_avail = False
GPS_avail = False
LIDAR1_avail = False
LIDAR2_avail = False
LTR_avail = False
TSL_avail = False
start_time = time.monotonic()
last_print = time.monotonic()

# Try to initialize IMU sensor
try:
    i2c = board.I2C()
    I2C_avail = True
except Exception as e:
    print(f"I2C initialization failed: {e}")
# If I2C available, initialize sensors
if I2C_avail:
    # Try to initialize LTR390
    try:
        ltr = adafruit_ltr390.LTR390(i2c)
        LTR_avail = True
    except Exception as e:
        print(f"LTR initialization failed: {e}")

    # Try to initialize TSL2591
    try:
        tsl = adafruit_tsl2591.TSL2591(i2c)
        TSL_avail = True
    except Exception as e:
        print(f"TSL initialization failed: {e}")
try:
    i2c1 = busio.I2C(scl=board.D4, sda=board.D7)
    I2C1_avail = True
    print("I2C1 Initialized")
except Exception as e:
    print(f"I2C1 initialization failed: {e}")
try:
    i2c2 = busio.I2C(scl=board.D12, sda=board.D13)
    I2C2_avail = True
    print("I2C2 Initialized")
except Exception as e:
    print(f"I2C2 initialization failed: {e}")
if I2C1_avail:
    # Try to initialize Lidar 1
    try:
        lidar1 = adafruit_lidarlite.LIDARLite(i2c1)
        LIDAR1_avail = True
    except Exception as e:
        print(f"Lidar 1 initialization failed: {e}")
if I2C2_avail:
    # Try to initialize Lidar 2
    try:
        lidar2 = adafruit_lidarlite.LIDARLite(i2c2)
        LIDAR2_avail = True
    except Exception as e:
        print(f"Lidar 2 initialization failed: {e}")
try:
    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,500")
    GPS_avail = True
except Exception as e:
    print(f"GPS initialization failed: {e}")
# Initialize the PIB class
pib = astrobotic_lib.PIB()
gps.update()
with open("/sd/ASTRO26.txt", "a") as f:
    f.write(
        "Elapsed Time, Daystamp, Hour, Minute, Second, Latitude, (Precise),"
        "Longitude, (Precise), Altitude, Speed, Fix Quality, Lidar 1, Lidar 2"
        "UV, UV Index, Amb Light, Lux,"
        "TSL Lux, TSL IR, TSL Visible, TSL Full Spectrum"
    )
# Main loop
while True:
    # Update the PIB state
    pib.update()
    gps.update()
    elapsed_time = time.monotonic() - start_time

    # Determine the file name based on the PBF state and duration
    if pib.pbf:
        file_name = "ASTRO26.txt"  # PBF is out
    elif pib.duration >= 20 * 60:
        file_name = "ASTRO26.txt"  # PBF is IN and ON for more than 20 minutes
    else:
        file_name = "testFlight.txt"  # PBF is IN but ON for less than 20 minutes
    current = time.monotonic()
    if current - last_print >= 0.5:
        last_print = current

        gps.update()
        # Read GPS sensor values if available
        if GPS_avail:
            gps.update()
            if gps.has_fix:
                daystamp = "{year}-{month}-{day}".format(
                    year=gps.timestamp_utc.tm_year,
                    month=gps.timestamp_utc.tm_mon,
                    day=gps.timestamp_utc.tm_mday,
                )
                hour = gps.timestamp_utc.tm_hour
                min = gps.timestamp_utc.tm_min
                sec = gps.timestamp_utc.tm_sec
                lat = gps.latitude_degrees
                lat_m = gps.latitude_minutes
                long = gps.longitude_degrees
                long_m = gps.longitude_minutes
                altitude = gps.altitude_m
                speed = gps.speed_knots
                fix_quality = gps.fix_quality
            else:
                daystamp = (
                    lat
                ) = (
                    lat_m
                ) = (
                    long
                ) = long_m = altitude = speed = fix_quality = hour = min = sec = "N/A"
        else:
            daystamp = (
                lat
            ) = (
                lat_m
            ) = (
                long
            ) = long_m = altitude = speed = fix_quality = hour = min = sec = "N/A"
        # Lidar 1 Data
        if LIDAR1_avail:
            try:
                dist1 = lidar1.distance
            except Exception as e:
                print(f"Lidar 1 data failed: {e}")
                dist1 = "TC"
        else:
            dist1 = "N/A"
        # Lidar 2 Data
        if LIDAR2_avail:
            try:
                dist2 = lidar2.distance
            except Exception as e:
                print(f"Lidar 2 data failed: {e}")
                dist1 = "TC"
        else:
            dist2 = "N/A"

        # Read LTR data
        if LTR_avail:
            uv = ltr.uvs
            amb = ltr.light
            uvi = ltr.uvi
            lux = ltr.lux
        else:
            uv = amb = uvi = lux = "N/A"
        # Read TSL data
        if TSL_avail:
            tsl_lux = tsl.lux
            tsl_ir = tsl.infrared
            tsl_v = tsl.visible
            tsl_fs = tsl.full_spectrum
        else:
            tsl_lux = tsl_ir = tsl_v = tsl_fs = "N/A"

        # Format the sensor data as a string
        data = (
            "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},"
            "{},{},{},{},{},{}\n".format(
                elapsed_time,
                daystamp,
                hour,
                min,
                sec,
                lat,
                lat_m,
                long,
                long_m,
                altitude,
                speed,
                fix_quality,
                dist1,
                dist2,
                uv,
                uvi,
                amb,
                lux,
                tsl_lux,
                tsl_ir,
                tsl_v,
                tsl_fs,
            )
        )

        # Store the sensor data
        pib.save_data(file_name, data)
        print(data)