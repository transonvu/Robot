from cleverwrap import CleverWrap
import speech_recognition as sr
from gtts import gTTS
import sys
import os

cw = CleverWrap("CC1jbQ1nO5wGPNeZ5UgNCKuhH5g")
r = sr.Recognizer()

while True:
    with sr.Microphone() as source:                                                                       
        print "Speak!"                                                                                   
        audio = r.listen(source) 
    try:
        print "You said " + r.recognize_google(audio)
    except sr.UnknownValueError:
        print "Could not understand audio"
    except sr.RequestError as e:
        print "Could not request results; {0}".format(e)
