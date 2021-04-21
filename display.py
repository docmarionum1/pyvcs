import numpy as np
import cv2
import time
import sys
import array
#from matplotlib import pyplot as plt
#import random
#print(plt.get_backend())


#plt.ioff()
#plt.show(block=False)

#resolution = (160, 192)
#resolution = (192, 160)
#resolution = (30, 40)
#resolution = (256, 256)
#resolution = (90, 160)
RESOLUTION = (108, 192)

#data = np.zeros( resolution + (3,), dtype=np.uint8).tolist()
#data = cv2.cr
data = [0] * (resolution[0] * resolution[1] * 3)
data = array.array('B', data)
#data = np.zeros((resolution[0] * resolution[1] * 3), dtype=np.uint8)

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

COLOR = [0, 0, 0]
BALLS = []
X = 0
Y = 0

class Ball:
    def __init__(self, width):#, color=None):
        self.width = width

        #if color:
        #    global COLOR
        #    COLOR = color
        self.enabled = False
        self.x = 0
        BALLS.append(self)

    def enable()



def main():
    start = time.time()
    batch_start = time.time()
    #print()
    i = 0
    while True:
    #for i in range(600):
        #print(np.random.randint([0, 0], data.shape[:2], size=2))


        #a = 100**i
        #b = a*a

        #for j in range(44032):
        for j in range(0, resolution[0]*resolution[1], 1):
            #print(j, [j & 256, (j & 0xFF00) >> 8, (j & 0xFF0000) >> 16])
            #data[int(j / 192), j % 192] = [255, 255, 0]
            #data[int(j / 192), j % 192] = [j & 0xff, (j & 0xFF00) >> 8, (j & 0xFF0000) >> 16]#np.random.randint(0, 255, 3)
            y = int(j / resolution[1])
            x = j % resolution[1]
            # np array
            #data[y, x, 0] = j & 0xff#, (j & 0xFF00) >> 8, (j & 0xFF0000) >> 16])
            #data[y, x, 1] = (j & 0xFF00) >> 8
            #data[y, x, 2] = (j & 0xFF0000) >> 16

            # python list of lists
            #data[y][x][0] = j & 0xff#, (j & 0xFF00) >> 8, (j & 0xFF0000) >> 16])
            #data[y][x][1] = (j & 0xFF00) >> 8
            #data[y][x][2] = (j & 0xFF0000) >> 16

            # Flat list or array.array (Slightly faster)
            #data[j*3] = j*2 & 0xff
            #data[j*3 + 1] = (j*2 & 0xFF00) >> 8
            #data[j*3 + 2] = (j*2 & 0xFF0000) >> 16
            data[j*3] = COLOR[0]
            data[j*3 + 1] = COLOR[1]
            data[j*3 + 2] = COLOR[2]
            #if j > 10:
            #    1/0

        #coords = np.random.randint([0, 0], data.shape[:2], size=2)
        #data[coords[0], coords[1]] = np.random.randint(0, 255, 3)

        cv2.imshow(
            "window",
            #cv2.resize(np.array(data, dtype=np.uint8).reshape(resolution + (3,)), (resolution[1]*4, resolution[0]*4))
            np.array(data, dtype=np.uint8).reshape(resolution + (3,))
        )
        #cv2.imshow("window", data.reshape(resolution + (3,)))
        #cv2.imshow("window", cv2.resize(data, (data.shape[1]*4, data.shape[0]*4), interpolation=cv2.INTER_NEAREST))
        cv2.waitKey(1)

        sys.stdout.write('\r')
        #sys.stdout.write("%.2f" % (i / time.time() - start))
        sys.stdout.write("%.2f %.2f" % (i / (time.time() - start), (i % 60) / (time.time() - batch_start)))
        sys.stdout.flush()
        i += 1

        if i % 60 == 0:
            batch_start = time.time()
        #plt.imshow(data)
        #plt.pause(0.000001)

if __name__ == '__main__':
    main()
