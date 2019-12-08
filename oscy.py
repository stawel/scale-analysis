#!/usr/bin/python
from pylab import *
import serial
from numpy import *
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import math
import collections


print "Setting up port"
port=serial.Serial('/dev/ttyUSB0',115200)
port.readline()
print "done"


xLen = 1024*10
avrLen = 100
xSmps = 80.0
yRange = 1000

yData = collections.deque(maxlen=xLen)
yAvrData = collections.deque(maxlen=xLen)
yAvrBuf = collections.deque(maxlen=avrLen)

def avr(y):
    return sum(y)/(len(y)*1.0)

def get_data(zero = 0.):
    for i in range(10):
        v = float(port.readline()) - zero
        yData.append(v)
        yAvrBuf.append(v)
        yAvrData.append(avr(yAvrBuf))


get_data()
yZero = avr(yData)
yData.clear()
yAvrBuf.clear()
yAvrData.clear()

fig1 = plt.figure()

plt.xlim(0, xLen/xSmps)
plt.ylim(-yRange, +yRange)
plt.xlabel('[s]')
plt.title('HX711')

l1, = plt.plot([], [], 'r-')
l2, = plt.plot([], [], 'g-')

def update_line(num):
    get_data(yZero)
    x = np.arange(len(yData))/xSmps
    l1.set_data(x, yData)
    l2.set_data(x, yAvrData)
    a = avr(yData)
    sigma = avr([(v - a)**2 for v in yData])**0.5
    print "sigma:", sigma, "\tAvr(", avrLen,"):", yAvrData[-1]



line_ani = animation.FuncAnimation(fig1, update_line, None,
    interval=10)
#, blit=True)
#line_ani.save('lines.mp4')


plt.show()


