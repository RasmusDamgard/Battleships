#-------------------------------------------------------------------------------
# Name:        Battleships - Blind Edition
# Purpose:     To help blind people
#
# Author:      Olipus & Mastercoder27
#
# Created:     30-01-2019
# Copyright:   (c) OLIVER 2019
# Licence:     We dont need a license, bitch lasagna
#-------------------------------------------------------------------------------
import speech_recognition as sr
from pygame import mixer

mixer.init()
mixer.music.load("coords6.wav")
mixer.music.play()

r = sr.Recognizer()

test = sr.AudioFile('coords6.wav')
with test as source:
    audio = r.record(source)

print(r.recognize_google(audio))
