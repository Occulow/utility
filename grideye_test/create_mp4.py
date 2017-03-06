# Creates <csv_file_name>.mp4

import sys
import numpy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation

def main():
  if len(sys.argv) < 2:
    print "Usage ./plot.py <csv_file_name>"

  metadata = dict(title="animation", artist="Occulow")
  FFMpegWriter = animation.writers['ffmpeg']
  writer = FFMpegWriter(fps=10, metadata=metadata)

  data = numpy.genfromtxt(sys.argv[1], delimiter=",")
  
  fig = plt.figure()
  ax = fig.add_subplot(111)
  im = ax.imshow(numpy.zeros((8,8)), cmap="hot")
  im.set_clim(0,10)
  
  # Show heatmap frame by frame, redrawing every 0.1 seconds (10 FPS)
  print "Writing to: " + sys.argv[1] + ".mp4"
  with writer.saving(fig, (sys.argv[1] + ".mp4"), 150):
    for i in range(len(data)):
      im.set_array(data[i].reshape((8,8)))
      writer.grab_frame()

if __name__ == "__main__":
  main()
    
