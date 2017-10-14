#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cleverwrap import CleverWrap
import speech_recognition as sr
from gtts import gTTS
import sys
import os
import subprocess
from mutagen.mp3 import MP3
from translation import bing
import serial
import re
import codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
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

cw = CleverWrap("CC1jbQ1nO5wGPNeZ5UgNCKuhH5g")
r = sr.Recognizer()
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    with sr.Microphone(device_index=2) as source:   
        r.adjust_for_ambient_noise(source)                                                                     
        print "Speak!"                                                                                   
        audio = r.listen(source) 
    try:
        vnrecognizetext = r.recognize_google(audio, language="vi-VN")
        print "You said " + vnrecognizetext
        enrecognizetext = bing(vnrecognizetext, dst = 'en')
    	enresponsetext = cw.say(enrecognizetext)
        vnresponsetext = bing(enresponsetext, dst = 'vi')
        print("Cleverbot: " + vnresponsetext)
        tts = gTTS(text=vnresponsetext, lang='vi')
    	tts.save("response.mp3")
        audio = MP3("response.mp3")
        print audio.info.length
    	os.system("mpg123 response.mp3")
	    ser.write(str(audio.info.length) + " " + convert(vnresponsetext) + "\n")
	
	while 1: 
		if ser.in_waiting:
	    	start = ser.readline()
			if start == "0\n":
				break;

    except sr.UnknownValueError:
        print "Could not understand audio"
    except sr.RequestError as e:
        print "Could not request results; {0}".format(e)
