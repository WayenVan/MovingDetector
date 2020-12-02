#this is a file to test what we design filter
from os import wait
import pickle 
import numpy as np
import sys
import time

sys.path.append("./webcam2rgb")
import webcam2rgb

dataclips = [[],[], []]

def callBack(retval, data):
    b = data[0]
    g = data[1]
    r = data[2]
    print("in")
    dataclips[0].append[b]
    dataclips[1].append[g]
    dataclips[2].append[r]


camera = webcam2rgb.Webcam2rgb()

#check the samplling rate of 
camera.start(callback = callBack, cameraNumber=0)

while 1:
    time.sleep(0.01)

print(dataclips)
f = open("./data/data_clip.dat", 'wb')
pickle.dump(dataclips, f)
f.close()



camera.stop()