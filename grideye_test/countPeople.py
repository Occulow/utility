# Run this on a host computer 

import sys
import numpy
<<<<<<< HEAD
import time
import matplotlib.pyplot as plt
import math
from matplotlib import animation
=======
import math
>>>>>>> 8292c0a5e743b056912c7354d97122f4cd6dca7d
from Queue import *

def count(q, data, maxValIn, In):
    count = 0
    listFrame = [] #to prevent double counting with consecutive frames
    pix = 0 if In else 7
    while not q.empty():
        i = q.get()
        for m in range(3, 10):
            if i+m < 100:
                frame = data[i+m].reshape((8,8))
                countPixel = 0
                for j in range(0, 8):
                    if frame[j][pix] >= maxValIn:
                        countPixel += 1
                if not listFrame or (listFrame[-1] != i-1  and listFrame[-1] != i):
                    if countPixel == 3:
                        count += 1
                        listFrame.append(i)
                    elif countPixel > 3:
                        count += 2
                        listFrame.append(i)
    return count



def main():
    if len(sys.argv) < 2:
        print "Usage ./plot.py <csv_file_name>"

    data = numpy.genfromtxt(sys.argv[1], delimiter=",")

    #create a queue for every person that walks in/out
    qIn = Queue() 
    qOut = Queue()

    maxValIn = 30.25
    maxValOut = 30.25
    for i in range(len(data)):
        frame = data[i].reshape((8,8))
        for j in range(0,8):
            if frame[j][7] >= maxValIn:
                qIn.put(i, False)
                break
            if frame[j][0] >= maxValOut:
                qOut.put(i, False) 
                break

   
    print 'countIn = ', count(qIn, data, maxValIn, True)
    print 'countOut = ',  count(qOut, data, maxValOut, False)

if __name__ == "__main__":
  main()
    
