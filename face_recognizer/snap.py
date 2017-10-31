#!/usr/bin/python

# Import the required modules
import cv2
import os
import numpy as np
import freenect
from PIL import Image

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array

path = './thinh'
count = 0
while 1:
    #get a frame from RGB camera
    frame = get_video()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #display RGB image
    cv2.imshow('RGB image', gray_frame)
    cv2.imwrite(path + "/16_" + str(count) + ".png", gray_frame) 
    count += 1
    # quit program when 'esc' key is pressed
    k = cv2.waitKey(3000) & 0xFF

    if k == 27 or count == 100:
        break
