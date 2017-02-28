# Run this on a host computer 

import numpy
import time
import matplotlib.pyplot as plt
from matplotlib import animation

data = numpy.genfromtxt("data.csv", delimiter=",")

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow(data[0].reshape((8,8)))
plt.show(block=False)


# Show heatmap frame by frame, redrawing every 0.1 seconds (10 FPS)
for i in range(len(data)):
  time.sleep(0.1)
  im.set_array(data[i].reshape((8,8)))
  fig.canvas.draw()
  

