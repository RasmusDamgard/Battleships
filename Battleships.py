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

alphabet = ["a","b","c","d","e","g","h","i","j","k","l","m","n","o",]

###
### Classes
###

class Board:
    def __init__(self, columns, rows, ships):
        # Create two identical two-dimensional array.
        self.visible = [[0 for rows in range(rows)] for cols in range(columns)]
        self.hidden = [[0 for rows in range(rows)] for cols in range(columns)]
        # Safe column and row information in this instance.
        self.columns = columns
        self.rows = rows
        self.ships = ships

    def draw_visible(self):
        for r in range(self.rows):
            for c in range(self.columns):
                print(self.visible[c][r], end=" ")
            print(" ")

    def draw_hidden(self):
        for r in range(self.rows):
            for c in range(self.columns):
                print(self.hidden[c][r], end=" ")
            print(" ")

    def add_ship(self, x, y, dirX, dirY, size, checkFirst = True):
        isValid = True
        if(x + dirX * size > self.columns):
            print("Out of bounds")
            return
        if(y + dirY * size > self.rows):
            print("Out of bounds")
            return
        if(self.ships < 1):
            print("All ships used")
            return
        for i in range(size):
            if(checkFirst == True):
                #If there is anything but water, its not valid.
                if(self.hidden[x-1+i*dirX][y-1+i*dirY] > 0):
                    isValid = False
            else:
                self.hidden[x-1+i*dirX][y-1+i*dirY] = self.ships
        if(isValid == False):
            print("Occupied")
            return
        if(checkFirst == True):
            self.add_ship(x, y, dirX, dirY, size, False)
        else:
            self.ships -= 1
            print("You succesfully placed a ship")

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
computerBoard = Board(10, 6, 5)

#Add a ship at [5,5] heading right [1,0] with size 3.
playerBoard.add_ship(9, 5, 1, 0, 3)
#This ship doesnt get placed because it overlaps with the other.
playerBoard.add_ship(3, 3, 0, 1, 4)
playerBoard.fire(5, 5)
playerBoard.fire(5, 6)
playerBoard.fire(5, 7)
playerBoard.fire(5, 8)

# Update gamescreen
computerBoard.draw_visible()
print("")
playerBoard.draw_hidden()
print("")
playerBoard.draw_visible()
print("")

print(computerBoard.columns)
print(computerBoard.rows)

# Prevent game from closing.
input("Exit Game?")
