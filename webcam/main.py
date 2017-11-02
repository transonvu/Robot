#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2
import thread
import urllib2

app = Flask(__name__)
video = cv2.VideoCapture(0)
image = None

def check_connected():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

def get_video():
    global image
    while 1:
        success, image = self.video.read()

def get_frame():
    global image
    ret, jpeg = cv2.imencode('.jpg', image)
    return jpeg.tobytes()

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

while not check_connected():
    pass
thread.start_new_thread(get_video, ())
app.run(host='192.168.20.120', port=4000, threaded=True)
video.release()