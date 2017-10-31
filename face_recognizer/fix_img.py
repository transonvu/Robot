#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
from PIL import Image

path = './thinh'
# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
image_paths = [os.path.join(path, f) for f in os.listdir(path)]
# images will contains face images
# labels will contains the label that is assigned to the image
for image_path in image_paths:
    # Read the image and convert to grayscale
    image_pil = Image.open(image_path).convert('L')
    # Convert the image format into numpy array
    image = np.array(image_pil, 'uint8')
    # Get the label of the image
    # Detect the face in the image
    faces = faceCascade.detectMultiScale(image)
    # If face is detected, append the face to images and the label to labels

    name = os.path.split(image_path)[1].split(".")
    print name
    #num = name[0].replace("subject", "")
    #typ = name[1]

    fname = name[0]
    print fname
    count = 0
    for (x, y, w, h) in faces:
        print count
        cv2.imwrite(fname + "_" + str(count) + ".png", image[y: y + h, x: x + w])
        count += 1
