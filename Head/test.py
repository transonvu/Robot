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

cw = CleverWrap("CC1jbQ1nO5wGPNeZ5UgNCKuhH5g")
r = sr.Recognizer()

vnrecognizetext = "Mày là ai"
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