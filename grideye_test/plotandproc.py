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


def checkFrame(frame, cellVal, In, listFrame, countOfFrame):
  pix = 4 if In else 3
  if not listFrame or (listFrame[-1] < countOfFrame-3):
    for j in xrange(0,8):
      if cellVal < 3:
        maxVal = cellVal - .8
        maxValUpDownCells = cellVal - 1.75
      else:
        maxVal = cellVal - .5
        maxValUpDownCells = cellVal - 1.0
      if frame[j][pix] >= maxVal:
        if j == 0 and frame[j+1][pix] >= maxValUpDownCells:
          listFrame.append(countOfFrame)
          return True
        elif j == 7 and frame[j-1][pix] >= maxValUpDownCells:
          listFrame.append(countOfFrame)
          return True
        elif ((j > 0 and frame[j-1][pix] >= maxValUpDownCells) or (j <7 and frame[j+1][pix] >= maxValUpDownCells)):
          listFrame.append(countOfFrame)
          return True
  return False



def count(cellVall, In, countOfFrame, countOut, countIn):
  pix = 4 if In else 3
  listFrame = []
  if frameCount >= 3:
      frame_1 = countBuff[-1]
      frame_2 = countBuff[-2]
      frame_3 = countBuff[-3]
      if checkFrame(frame_1, cellVall, In, listFrame, countOfFrame):
        if In:
          countIn += 1
        else:
          countOut += 1
      elif checkFrame(frame_2, cellVall, In, listFrame, countOfFrame):
        if In:
          countIn += 1
        else:
          countOut += 1
      elif checkFrame(frame_3, cellVall, In, listFrame, countOfFrame):
        if In:
          countIn += 1
        else:
          countOut += 1
  return (countIn, countOut)






def countPeople(frame, countOfFrame, countOut, countIn):
  maxValIn = 2.5
  maxValInUpDownCells = 1.7
  maxValOutUpDownCells = 1.5
  maxValOut = 2.5
  frameInPut = False
  frameOutPut = False

  for j in range(0,8):
    if frame[j][2] >= maxValIn and not frameInPut:
      cellVal = frame[j][2]
      if j == 0 and frame[j+1][2] >= maxValInUpDownCells:
        frameInPut = True
        (countIn, countOut) = count(cellVal, True, countOfFrame, countOut, countIn)
      elif j == 7 and frame[j-1][2] >= maxValInUpDownCells:
        frameInPut = True
        (countIn, countOut) = count(maxValIn, True, countOfFrame, countOut, countIn)
      elif  (j > 0 and frame[j-1][2] >= maxValInUpDownCells) or (j < 7 and frame[j+1][4] >= maxValInUpDownCells):
        frameInPut = True
        (countIn, countOut) = count(maxValIn, True, countOfFrame, countOut, countIn)

    if frame[j][5] >= maxValOut and not frameOutPut:
      cellVal = frame[j][5]
      if j == 0 and frame[j+1][5] >= maxValOutUpDownCells:
        frameOutPut = True
        (countIn, countOut) = count(maxValOut, False, countOfFrame, countOut, countIn)
      elif j == 7 and frame[j-1][5] >= maxValOutUpDownCells:
        frameOutPut = True
        (countIn, countOut) = count(maxValOut, False, countOfFrame, countOut, countIn)
      elif  (j > 0 and frame[j-1][5] >= maxValOutUpDownCells) or (j < 7 and frame[j+1][3] >= maxValOutUpDownCells):
        frameOutPut = True
        (countIn, countOut) = count(maxValOut, False, countOfFrame, countOut, countIn)
  return (countIn, countOut)


# current_time = datetime.datetime.now()
# last_time = current_time
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

        if frameCount < 4:
          countBuff.append(filtered_val)
        else:
          countBuff = countBuff[1::]
          countBuff.append(filtered_val)
          startIndex = frameCount - 3

        (countIn, countOut) = countPeople(filtered_val, frameCount, countOut, countIn)
        print 'countIn: ', countIn
        print 'countOut: ', countOut

        writer_med.writerow(filtered_val.flatten())

        fig.canvas.draw()

        
        # Print FPS
        # current_time = datetime.datetime.now()
        # print str(1000000/(current_time - last_time).microseconds) + " FPS"
        # last_time = current_time
  
