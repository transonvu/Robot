from cleverwrap import CleverWrap
import speech_recognition as sr
from gtts import gTTS
import sys
import os

cw = CleverWrap("CC1jbQ1nO5wGPNeZ5UgNCKuhH5g")
r = sr.Recognizer()

while True:
    with sr.WavFile("record.wav") as source: # use "test.wav" as the audio source
        audio = r.record(source)     
    try:
    	vnrecognizetext = r.recognize_google(audio, language="vi-VN")
    except sr.UnknownValueError:
    	print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
    	print("Could not request results from Google Speech Recognition service; {0}".format(e))