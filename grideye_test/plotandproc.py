import serial
import datetime
import random
import csv
import numpy
import time
from Queue import *
import matplotlib.pyplot as plt

MEDIAN_FILTER_SIZE = 10

ser = serial.Serial()
ser.port = "/dev/tty.usbmodem1412"
ser.baudrate = 115200
ser.dsrdtr = True

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow(numpy.zeros((8,8)), cmap="hot", interpolation="nearest")
history = numpy.empty((8,8,1))
plt.show(block=False)
frameCount = 0

im.set_clim(0,10)

ser.open()

countBuff =[]
startIndex = 0
countOut = 0
countIn = 0


t = str(int(round(time.time() * 1000))) 
fname = t + ".log.csv"
fname_med = t + "-median" + ".log.csv"

def count(maxVal, In, countOfFrame, countOut, countIn):
  pix = 0 if In else 7
  print "within count"
  if frameCount >= 10:
    print "In count"
    index = 0
    for m in range(3,8):
      frameToCheck = countBuff[index+m].reshape((8,8))
      countPixel = 0
      print "set countPixel"
      for j in range(0, 8):
        print "frameToCheck value = ", frameToCheck[j][pix]
        if frameToCheck[j][pix] >= maxVal:
          print "within countPixel"
          countPixel += 1
          if countPixel == 3: 
            print "within pizek == 3"
            if In:
              countIn += 1
            else:
              countOut += 1
  return (countIn, countOut)

def countPeople(frame, countOfFrame, countOut, countIn):
  maxValIn = 2.0
  maxValOut = 2.0
  for i in xrange(8):
    if frame[i][7] >= maxValIn:
      print "In count people before calling CountIn. Value = ", frame[i][7]
      (countIn, countOut) = count(maxValIn, True, countOfFrame, countOut, countIn)
      break
    if frame[i][0] >= maxValOut:
      (countIn, countOut) = count(maxValOut, False, countOfFrame, countOut, countIn)
      break
  return (countIn, countOut)


# current_time = datetime.datetime.now()
with open(fname_med, 'w') as med_file:
  with open(fname, 'w') as csv_file:
      writer = csv.writer(csv_file, delimiter=',')
      writer_med = csv.writer(med_file, delimiter=',')
      while True:
        data = ser.readline()
        frame = numpy.fromstring(data, sep=",").reshape((8,8)) * 0.25
        
        # Write to csv
        writer.writerow(frame.flatten())

        history = numpy.dstack((frame, history))[:,:,0:MEDIAN_FILTER_SIZE]

        filtered_val = frame - numpy.median(history, axis=2)
        im.set_array(filtered_val)

        frameCount += 1

        if frameCount < 10:
          countBuff.append(filtered_val)
        else:
          countBuff = countBuff[1::]
          countBuff.append(filtered_val)
          startIndex = frameCount - 10

        (countIn, countOut) = countPeople(filtered_val, frameCount, countOut, countIn)
        print 'countIn: ', countIn
        print 'countOut: ', countOut

        writer_med.writerow(filtered_val.flatten())

        fig.canvas.draw()

        
        # Print FPS
        #current_time = datetime.datetime.now()
        #print str(1000000/(current_time - last_time).microseconds) + " FPS"
        #last_time = current_time
  
