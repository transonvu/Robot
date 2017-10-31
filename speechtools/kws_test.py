#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================================================
# Copyright (c) 2013 Carnegie Mellon University.  All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer. 
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# This work was supported in part by funding from the Defense Advanced 
# Research Projects Agency and the National Science Foundation of the 
# United States of America, and the CMU Sphinx Speech Consortium.
#
# THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND 
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
# NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ====================================================================


import sys, os
import datetime
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import speech_recognition as sr
from subprocess import call
from gtts import gTTS
#import Serial
from mutagen.mp3 import MP3
import re
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import thread
from Neri import Neri
import json
import httplib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
neri = Neri()

#serial = Serial.Serial()
# Import the required modules

modeldir = "/usr/local/lib/python2.7/dist-packages/pocketsphinx/model"
datadir = "/usr/local/lib/python2.7/dist-packages/pocketsphinx/data"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
config.set_string('-dict', os.path.join(modeldir, 'cmudict-en-us.dict'))
#config.set_string('-keyphrase', 'kitty')
config.set_float('-kws_threshold', 1e-20)

decoder = Decoder(config)

decoder.set_kws("kitty","kitty.txt")

jsgf2 = Jsgf('aeiou.gram')
rule2 = jsgf2.get_rule('aeiou.aeiou')
fsg2 = jsgf2.build_fsg(rule2, decoder.get_logmath(), 7.5)
fsg2.writefile('aeiou.fsg')
decoder.set_fsg("aeiou", fsg2)


# Open file to read the data
#stream = open(os.path.join(datadir, "goforward.raw"), "rb")

# Alternatively you can read from microphone
import pyaudio
# 
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

google_decoder = sr.Recognizer()


def do_rec_data(data):
    audio = sr.AudioData(''.join(data), 16000, 2)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        s = google_decoder.recognize_google(audio)
        return s
    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("......")
    return ""


def do_rec():

    bufs = []

    decoder.set_search("aeiou")
    decoder.start_utt()

    print "recording ..."
    count = 0
    sil_dur = 20
    max_dur = 80
    min_dur = 30
    in_speech = sil_dur
    while True:
        buf = stream.read(1024)
        decoder.process_raw(buf, False, False)

        if decoder.hyp() != None:
            in_speech = sil_dur  # silence duration
        else:
            if in_speech>0:
                in_speech = in_speech -1
        

        bufs.append(buf)
        count = count + 1
        if count > max_dur:  # max duration
            break
        elif count > min_dur:    # min duration
            if in_speech<1:
                break
        else:
            in_speech = sil_dur
    decoder.end_utt()    
    print "decoding ..."
    audio = sr.AudioData(''.join(bufs), 16000, 2)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        s = google_decoder.recognize_google(audio, None, "vi")
        print(s)
        return s
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return ""

patterns = {
    u'[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    u'[đ]': 'd',
    u'[èéẻẽẹêềếểễệ]': 'e',
    u'[ìíỉĩị]': 'i',
    u'[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    u'[ùúủũụưừứửữự]': 'u',
    u'[ỳýỷỹỵ]': 'y'
}


def convert(text):
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def do_nlu(text):
    text = text.lower().encode('utf8')
    question, answer, score = neri.ask(text)

    cmd = "chào"
    if score.find(cmd)>=0:
        conn = httplib.HTTPConnection(host='192.168.20.120', port=3000)
        conn.request('POST', '/face_recognizer')
        response = conn.getresponse()
        data = response.read()
        if data == 1:
            answer = "Chào Thịnh"

    tts = gTTS(text=answer.decode("utf8"), lang='vi')
    tts.save("out.mp3")
    call(["mpg123","out.mp3"])
    audio = MP3("out.mp3")
    print answer
    socketio.emit('ques', {'ques': question})
    socketio.emit('ans', {'ans': answer})
    
    # serial.sendMessage(str(audio.info.length) + "|" + "xinchao" + "|" + "xinchao")
    # isStop = False
    # while isStop == False:
    #     while serial.inWaiting():
    #         s = serial.readMessage()
    #         if  s.find("OK") != -1:
    #             isStop = True
    #             break

    # cmd = "mấy giờ rồi"
    # if text.find(cmd)>=0:
    #     t = datetime.datetime.now()
    #     s = str(t.hour) + ":" + str(t.minute)
    #     tts = gTTS(text=s, lang='vi')
    #     tts.save("out.mp3")
    #     audio = MP3("out.mp3")
    #     call(["mpg123","out.mp3"])
    
    # cmd = "bạn có thể làm gì"
    # if text.find(cmd)>=0:
    #     s = u"tôi có thể làm giám đốc công ty golden eye thay anh An"
    #     tts = gTTS(text=s, lang='vi')
    #     tts.save("out.mp3")
    #     call(["mpg123","out.mp3"])
        
    # cmd = "xin chào"
    # if text.find(cmd)>=0:
    #     socketio.emit('ques', {'ques': 'xin chào'})
    #     socketio.emit('ans', {'ans': 'xin chào'})

    #     s = u"xin chào"
    #     tts = gTTS(text=s, lang='vi')
    #     tts.save("out.mp3")
    #     call(["mpg123","out.mp3"])
    #     audio = MP3("out.mp3")
    #     print "convert ", convert(s)
        # serial.sendMessage(str(audio.info.length) + "|" + "xinchao" + "|" + "xinchao")
        # isStop = False
        # while isStop == False:
        #     while serial.inWaiting():
        #         s = serial.readMessage()
        #         if  s.find("OK") != -1:
        #             isStop = True
        #             break

       
def listening():
    # Process audio chunk by chunk. On keyword detected perform action and restart search
    decoder.set_search("kitty")
    decoder.start_utt()

    print "listening keyword kitty"

    data = []
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
            if len(data)>20:
                data.pop(0)
            data.append(buf)

        else:
            break
        if decoder.hyp() != None:
            end_utt = False
            for seg in decoder.seg():
                #print ("Detected keyword, restarting search")
                print seg.word
                if (seg.word.find("kitty")>=0):
                
                    if len(data)>10:
                        s = do_rec_data(data)
                        s = s.lower()
                        print s
                        # data = []
                        if s.find("kitty")>=0:
                            print "keyword is detected"
                            call(["aplay","aha.wav"])
                            decoder.end_utt()
                            end_utt = True
                            out = do_rec()
                            do_nlu(out)
                            data = []
                            break
                        else:
                            print "false alarm"
                            socketio.emit('ques', {'ques': 'đang nghe ...'})
                            socketio.emit('ans', {'ans': ''})

                    else:
                        print "audio too short"
            if not end_utt:
                decoder.end_utt()
            decoder.set_search("kitty")
            decoder.start_utt()
            print "listening keyword kitty"
        
@socketio.on('connect')
def test_connect():
    print('Client connected!')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected!')

thread.start_new_thread(listening, ())
socketio.run(app, host='192.168.20.120', port=3001)