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
        self.visible = [[0 for cols in range(columns)] for rows in range(rows)]
        self.hidden = [[0 for cols in range(columns)] for rows in range(rows)]
        # Safe column and row information in this instance.
        self.columns = columns
        self.rows = rows
        self.ships = ships

    def draw_visible(self):
        for c in range(self.columns):
            for r in range(self.rows):
                print(self.visible[r][c], end=" ")
            print(" ")

    def draw_hidden(self):
        for c in range(self.columns):
            for r in range(self.rows):
                print(self.hidden[r][c], end=" ")
            print(" ")

    def add_ship(self, x, y, direction, length):
        if(direction == "right"):
            for i in range(length):
                self.hidden[x-1+i][y-1] = self.ships
        if(direction == "left"):
            for i in range(length):
                self.hidden[x-1-i][y-1] = self.ships
        if(direction == "up"):
            for i in range(length):
                self.hidden[x-1][y-1-i] = self.ships
        if(direction == "down"):
            for i in range(length):
                self.hidden[x-1][y-1+i] = self.ships
        self.ships -= 1

    def fire(self, x, y):
        target = self.visible[x-1][y-1]
        #Checks if there has already been fired at this square.
        if(target == 0): #Have not fired before.
            hit = self.hidden[x-1][y-1]
            #Checks what was hit.
            if(hit == 0): #Water
                self.visible[x-1][y-1] = 1
                print("Miss!")
            else: #A ship
                self.visible[x-1][y-1] = 2
                typeHit = self.hidden[x-1][y-1]
                self.hidden[x-1][y-1] += 10
                print("Hit!")
                self.checkDestroyed(typeHit)

        else: #Have already fired here.
            print("Already fired here")

    def checkDestroyed(self, typeHit):
        print("")
        if(any(typeHit in sublist for sublist in self.hidden) == False):
            for c in range(self.columns):
                for r in range(self.rows):
                    if(self.hidden[r][c] == typeHit + 10):
                        self.visible[r][c] = 3
            print("Destroyed a ship")


###
### Code for execution
###


playerBoard = Board(10, 10, 5)
computerBoard = Board(6, 6, 5)

playerBoard.add_ship(5, 5, "down", 3)
playerBoard.fire(5, 5)
playerBoard.fire(5, 6)
playerBoard.fire(5, 7)

# Update gamescreen
computerBoard.draw_visible()
print("")
playerBoard.draw_hidden()
print("")
playerBoard.draw_visible()
print("")

# Prevent game from closing.
input("Exit Game?")
