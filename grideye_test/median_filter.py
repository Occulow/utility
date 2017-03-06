# Takes a median filter of the input data and writes it to the output_file.
# This script also shows the conversion in real time.

import sys
import serial
import datetime
import random
import csv
import numpy
import time
import matplotlib.pyplot as plt

MEDIAN_FILTER_SIZE = 10

def main():
  if len(sys.argv) < 3:
    print "Usage ./plot.py <csv_file_name> <output_file_name>"

  data = numpy.genfromtxt(sys.argv[1], delimiter=",")
  
  fig = plt.figure()
  ax = fig.add_subplot(111)
  im = ax.imshow(data[0].reshape((8,8)), cmap="hot", interpolation="nearest")
  history = numpy.empty((8,8,1))
  plt.show(block=False)

  im.set_clim(0,10)
  
  fname_med = sys.argv[2]
  with open(fname_med, 'w') as med_file:
    writer_med = csv.writer(med_file, delimiter=',')
    # Shows conversion at 100x speed
    for i in range(len(data)):
      time.sleep(0.001)
      
      frame = data[i].reshape((8,8))
      history = numpy.dstack((frame, history))[:,:,0:MEDIAN_FILTER_SIZE]
      filtered_val = frame - numpy.median(history, axis=2)

      writer_med.writerow(filtered_val.flatten())
      
      im.set_array(filtered_val)
      fig.canvas.draw()


if __name__ == "__main__":
  main()
    

