#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      OLIVER
#
# Created:     30-01-2019
# Copyright:   (c) OLIVER 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import speech_recognition as sr

r = sr.Recognizer()

harvard = sr.AudioFile('test.wav')
with harvard as source:
    audio = r.record(source)

print(r.recognize_google(audio))

input("")