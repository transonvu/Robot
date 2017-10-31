#!/usr/bin/python

# Import the required modules
import cv2
import os
import numpy as np
import freenect
import cv2gpu
from PIL import Image

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadeCudaPath = "haarcascade_frontalface_default_cuda.xml"
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array


def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.tst')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split("_")[0])
        print image_path, nbr
        images.append(image)
        labels.append(nbr)
    # return the images list and labels list
    return images, labels

# Path to the Dataset
path = './faces'
# Call the get_images_and_labels function and get the face images and the 
# corresponding labels
images, labels = get_images_and_labels(path)

# Perform the tranining
recognizer.train(images, np.array(labels))

# # Append the images with the extension .sad into image_paths
# image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.tst')]
# for image_path in image_paths:
#     predict_image_pil = Image.open(image_path).convert('L')
#     predict_image = np.array(predict_image_pil, 'uint8')
#     faces = faceCascade.detectMultiScale(predict_image)
#     for (x, y, w, h) in faces:
#         nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
#         nbr_actual = int(os.path.split(image_path)[1].split("_")[0][-1])
#         if nbr_actual == nbr_predicted:
#             print "{} is Correctly Recognized with confidence {}".format(nbr_actual, conf)
#         else:
#             print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)

while 1:
    #get a frame from RGB camera
    frame = get_video()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray_frame, minSize=(60, 60))
    print "1"

    # If face is detected, append the face to images
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(gray_frame[y: y + h, x: x + w])
        print nbr_predicted, conf
	if nbr_predicted == 16 and conf >= 40 and conf <= 100:
            cv2.rectangle(frame, (x ,y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.rectangle(frame, (x ,y), (x + w, y + h), (255, 0, 0), 2)            

    #display RGB image
    cv2.imshow('RGB image', frame)
 
    # quit program when 'esc' key is pressed
    k = cv2.waitKey(1) & 0xFF

    if k == 27:
        break
