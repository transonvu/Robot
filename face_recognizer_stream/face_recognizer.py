#!/usr/bin/env python

from flask import Flask, render_template, Response
import cv2
import cv2gpu
import os
import numpy as np
import freenect
from PIL import Image

app = Flask(__name__)

cascadePath = "haarcascade_frontalface_default.xml"
#faceCascade = cv2.cuda.CascadeClassifier(cascadePath)
cv2gpu.init_gpu_detector(cascadePath)

recognizer = cv2.createLBPHFaceRecognizer()

def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array

def get_detect_video():
    img = get_video()
    faces = cv2gpu.find_faces(img)
    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = faceCascade.detectMultiScale(gray_img, minSize=(60, 60))

    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(gray_img[y: y + h, x: x + w])
	if nbr_predicted == 16 and conf >= 40 and conf <= 100:
            cv2.rectangle(img, (x ,y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.rectangle(img, (x ,y), (x + w, y + h), (255, 0, 0), 2)            

    return img

def get_frame(img):
    ret, jpeg = cv2.imencode('.jpg', img)
    return jpeg.tobytes()

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.tst')]
    images = []
    labels = []
    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = np.array(image_pil, 'uint8')
        nbr = int(os.path.split(image_path)[1].split("_")[0])
        print image_path, nbr
        images.append(image)
        labels.append(nbr)
    return images, labels

path = './faces'
images, labels = get_images_and_labels(path)
recognizer.train(images, np.array(labels))

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        frame = get_frame(get_detect_video())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='192.168.20.120', port=3000, threaded=True)

