# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import busio
import gc

def with_uart(callback):
    uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=2)
    try:
        distance = callback(uart)
        return distance
    finally:
        uart.deinit()
        del uart
        gc.collect()

def TF03_Distance_Read(uart):
    data = bytearray(9)  # TF03 sends 9 bytes per frame
    TIMER = time.time()
    while True and (time.time()-TIMER < 2):
        num_bytes = uart.readinto(data)

        if num_bytes == 9:
            if data[0] == 0x59 and data[1] == 0x59:
                # Parse distance from bytes 2 and 3
                distance = data[2] + (data[3] << 8)  # Little-endian

                # Validate checksum
                checksum = sum(data[:8]) & 0xFF
                if checksum == data[8]:
                    return distance
                else:
                    print("Checksum error!")
                    return None

        # Clear buffer to make room for next reading
        uart.reset_input_buffer()

        time.sleep(0.1)
    return None
