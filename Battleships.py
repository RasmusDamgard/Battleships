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

#Declare and initiate PyGame Mixer.
mixer.init()

#Declare speech recognizer software.
r = sr.Recognizer()

def Board(size):
    for columns in range(size[0]):
        for rows in range(size[1]):
            print ("# ", end=" ")
        print(" ")


Board([5,10])

#Prevent game from closing.
input("Exit Game?")