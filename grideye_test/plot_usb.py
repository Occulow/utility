import serial
import datetime
import random
import csv
import numpy
import time
from Queue import *
import matplotlib.pyplot as plt
from people_count import PeopleCounter

MEDIAN_FILTER_SIZE = 10

ser = serial.Serial()
ser.port = "/dev/tty.usbserial-AL02W6N5"
ser.baudrate = 115200
ser.dsrdtr = True

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow(numpy.zeros((8,8)), cmap="hot", interpolation="nearest")
history = numpy.empty((8,8,1))
plt.show(block=False)
frameCount = 0

im.set_clim(0,40)

ser.open()
countIn = 0.0
countOut = 0.0

t = str(int(round(time.time() * 1000))) 
fname = t + ".log.csv"
fname_med = t + "-median" + ".log.csv"

counter = PeopleCounter()


current_time = datetime.datetime.now()
last_time = current_time
ser.readline()
ser.readline()
ser.readline()
with open(fname_med, 'w') as med_file:
    writer = csv.writer(med_file, delimiter=',')
    while True:
        data = ser.readline()
        if data[0] == "D":
            # Print info out
            # print data
            counts = data[2:-3]
            counts = counts.split(",")
            (inDelta, outDelta) = map(float, counts)
            countIn += inDelta
            countOut += outDelta
            print "countIn = ", countIn
            print "countOut = ", countOut
        elif data[0] == "F":
            colon_index = data.find(":")
            frame = data[1:colon_index]
            # print data
            frame = numpy.fromstring(data[colon_index+1:], sep=",").reshape((8,8))
            writer.writerow(frame.flatten())
            im.set_array(frame)
            fig.canvas.draw()
            # Print FPS
            # current_time = datetime.datetime.now()
            # print str(1000000/(current_time - last_time).microseconds) + " FPS"
            # last_time = current_time
        else:
            print data
  
