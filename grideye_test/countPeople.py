# Run this on a host computer 

import sys
import numpy
import time
import math
from Queue import *

# values for first-median
# maxValIn = 2.5
# maxValInUpDownCells = 1.7
# maxValOutUpDownCells = 1.7
# maxValOut = 2.3

# values for third-median
# maxValIn = 2.5
# maxValInUpDownCells = 1.7
# maxValOutUpDownCells = 1.5
# maxValOut = 2.5


def checkFrame(frame, cellVal, In, data, listFrame, i, frameNum):
    pix = 4 if In else 3
    if not listFrame or (listFrame[-1] < i-3):
        # print "frame being checked = ", frameNum
        # print frame
        for j in xrange(0,8):
            putInList = False
            if cellVal < 3:
                maxVal = cellVal - .8
                maxValUpDownCells = cellVal - 1.75
            else:
                maxVal = cellVal - .5
                maxValUpDownCells = cellVal - 1.0
            if frame[j][pix] >= maxVal:
                if j == 0 and frame[j+1][pix] >= maxValUpDownCells and not putInList:
                    # print "in check 1"
                    listFrame.append(i)
                    putInList = True
                    return True
                elif j == 7 and frame[j-1][pix] >= maxValUpDownCells and not putInList:
                    # print "in check 2"
                    listFrame.append(i)
                    putInList = True
                    return True
                elif (frame[j-1][pix] >= maxValUpDownCells or frame[j+1][pix] >= maxValUpDownCells) and not putInList:
                    # print "in check 3"
                    listFrame.append(i)
                    putInList = True
                    return True
                else: 
                    return False
    return False



def count(q, data, In):
    count = 0
    listFrame = [] #to prevent double counting with consecutive frames
    while not q.empty():
        (i,cellVal) = q.get()
        if i > 3:
            # print "i = ", i, "In = ", In
            frame = data[i].reshape((8,8))
            # print frame
            frame_1 = data[i-1].reshape((8,8))
            frame_2 = data[i-2].reshape((8,8))
            frame_3 = data[i-3].reshape((8,8))
            if checkFrame(frame_1, cellVal, In, data, listFrame, i, i-1):
                # print "Adding for frame = ", i, "in checkFrame 1"
                count += 1
            elif checkFrame(frame_2, cellVal, In, data, listFrame, i, i-2):
                # print "Adding for frame = ", i, "in checkFrame 2"
                count += 1
            elif checkFrame(frame_3, cellVal, In, data, listFrame, i, i-3):
                # print "Adding for frame = ", i, "in checkFrame 3"
                count += 1
    return count




        



def main():
    if len(sys.argv) < 2:
        print "Usage ./plot.py <csv_file_name>"

    data = numpy.genfromtxt(sys.argv[1], delimiter=",")

    #create a queue for every person that walks in/out
    qIn = Queue() 
    qOut = Queue()

    maxValIn = 2.5
    maxValInUpDownCells = 1.7
    maxValOutUpDownCells = 1.5
    maxValOut = 2.5

    for i in range(len(data)):
        frame = data[i].reshape((8,8))
        frameInPut = False
        frameOutPut = False
        for j in range(0,8):
            if frame[j][2] >= maxValIn and not frameInPut:
                cellVal = frame[j][2]
                if j == 0 and frame[j+1][2] >= maxValInUpDownCells:
                    # print "for putting in qIn:  i = ", i
                    # print frame
                    qIn.put((i, cellVal), False)
                    frameInPut = True
                elif j == 7 and frame[j-1][2] >= maxValInUpDownCells:
                    # print "for putting in qIn:  i = ", i
                    # print frame
                    qIn.put((i, cellVal), False)
                    frameInPut = True
                elif  (j > 0 and frame[j-1][2] >= maxValInUpDownCells) or (j < 7 and frame[j+1][4] >= maxValInUpDownCells):
                    # print "for putting in qIn:  i = ", i
                    # print frame
                    qIn.put((i, cellVal), False)
                    frameInPut = True
            if frame[j][5] >= maxValOut and not frameOutPut:
                cellVal = frame[j][5]
                # print "Considering putting in qOut:  i = ", i
                # print frame
                if j == 0 and frame[j+1][5] >= maxValOutUpDownCells:
                    # print "for putting in qOut:  i = ", i
                    # print frame
                    qOut.put((i, cellVal), False)
                    frameOutPut = True
                elif j == 7 and frame[j-1][5] >= maxValOutUpDownCells:
                    # print "for putting in qOut:  i = ", i
                    # print frame
                    qOut.put((i, cellVal), False)
                    frameOutPut = True
                elif  (j > 0 and frame[j-1][5] >= maxValOutUpDownCells) or (j < 7 and frame[j+1][3] >= maxValOutUpDownCells):
                    # print "for putting in qOut:  i = ", i
                    # print frame
                    qOut.put((i, cellVal), False)
                    frameOutPut = True
                

    countIn = count(qIn, data, True)
    countOut = count(qOut, data, False)
   
    print 'countIn = ', countIn
    print 'countOut = ',  countOut

if __name__ == "__main__":
  main()
    
