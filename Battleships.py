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
import numpy as np
from pygame import mixer

###
### Variables and modules
###

# Declare and initiate PyGame Mixer.
mixer.init()

# Declare speech recognizer software.
r = sr.Recognizer()

###
### Classes
###

class Board:
    def __init__(self, columns, rows, ships):
        # Create two identical two-dimensional array.
        self.state = [[0 for cols in range(columns)] for rows in range(rows)]
        self.layout = [[0 for cols in range(columns)] for rows in range(rows)]
        # Safe column and row information in this instance.
        self.columns = columns
        self.rows = rows
        self.ships = ships

    def draw_state(self):
        for c in range(self.columns):
            for r in range(self.rows):
                print(self.state[r][c], end=" ")
            print(" ")

    def draw_layout(self):
        for c in range(self.columns):
            for r in range(self.rows):
                print(self.layout[r][c], end=" ")
            print(" ")

    def add_ship(self, x, y, direction, length):
        if(direction == "right"):
            for i in range(length):
                self.layout[x-1+i][y-1] = self.ships
        if(direction == "left"):
            for i in range(length):
                self.layout[x-1-i][y-1] = self.ships
        if(direction == "up"):
            for i in range(length):
                self.layout[x-1][y-1-i] = self.ships
        if(direction == "down"):
            for i in range(length):
                self.layout[x-1][y-1+i] = self.ships
        self.ships -= 1

    def fire(self, x, y):
        target = self.state[x-1][y-1]
        #Checks if there has already been fired at this square.
        if(target == 0): #Have not fired before.
            hit = self.layout[x-1][y-1]
            #Checks what was hit.
            if(hit == 0): #Water
                self.state[x-1][y-1] = 1
                print("Miss!")
            else: #A ship
                self.state[x-1][y-1] = 2
                self.layout[x-1][y-1] = 1
                print("Hit!")
        else: #Have already fired here.
            print("Already fired here")


###
### Code for execution
###


playerBoard = Board(10, 10, 5)
computerBoard = Board(6, 6, 5)

playerBoard.add_ship(5, 5, "down", 3)
playerBoard.fire(5, 6)
playerBoard.fire(1, 1)

# Update gamescreen
computerBoard.draw_state()
print("")
playerBoard.draw_layout()
print("")
playerBoard.draw_state()
print("")

# Prevent game from closing.
input("Exit Game?")
