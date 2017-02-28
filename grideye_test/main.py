#!/usr/bin/python

# Run this on a pi with a grideye connected via i2c
# Written for a raspberry pi 1, rev 1

import smbus
import csv
import time

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

FPS = 10  # Frames per second (10 is max from the grideye)
TIME_S = 10  # Length of data capture (in seconds)

DEVICE_ADDRESS = 0x68

REG_THERM_LSB = 0x0E
REG_THERM_MSB = 0x0F
REG_PIXEL_BASE = 0x80

# Write a single register
therm_lsb = bus.read_byte_data(DEVICE_ADDRESS, REG_THERM_LSB)
therm_msb = bus.read_byte_data(DEVICE_ADDRESS, REG_THERM_MSB)

temp = ((therm_msb << 8) + therm_lsb)
print("It is %f degrees Celcius." % (temp * 0.0625))

# Gets a frame of data from the sensor
def get_frame():
  pixels = []

  for i in range(8):
    row = []
    for j in range(8):
      lsb = bus.read_byte_data(DEVICE_ADDRESS, REG_PIXEL_BASE + 2*(8*i + j))
      msb = bus.read_byte_data(DEVICE_ADDRESS, REG_PIXEL_BASE + 2*(8*i + j) + 1)
      pixels.append(((msb << 8) + lsb) * 0.25)
  return pixels


# Gets a frame every 0.1 second (10 FPS)
arr = []
for i in range(FPS * TIME_S):
  arr.append(get_frame())
  time.sleep(1.0/FPS)

# Write to data.csv
with open("data.csv", "wb") as csvfile:
  writer = csv.writer(csvfile, delimiter=",")
  for row in arr:
    writer.writerow(row)

