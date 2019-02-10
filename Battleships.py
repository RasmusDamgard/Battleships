#-------------------------------------------------------------------------------
# Name:        BattleshipNum - Blind Edition
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
### Classes & Functions
###

class Board:
    def __init__(self, columns, rows, shipArray):
        # Create two identical two-dimensional array.
        self.visible = [[0 for rows in range(rows)] for cols in range(columns)]
        self.hidden = [[0 for rows in range(rows)] for cols in range(columns)]
        # Safe column and row information in this instance.
        self.columns = columns
        self.rows = rows
        self.shipArray = shipArray
        self.shipNum = sum(self.shipArray)

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
        if(self.shipNum < 1):
            print("All shipNum used")
            return
        for i in range(size):
            if(checkFirst == True):
                #If there is anything but water, its not valid.
                if(self.hidden[x-1+i*dirX][y-1+i*dirY] > 0):
                    isValid = False
            else:
                self.hidden[x-1+i*dirX][y-1+i*dirY] = self.shipNum
        if(isValid == False):
            print("Occupied")
            return
        if(checkFirst == True):
            self.add_ship(x, y, dirX, dirY, size, False)
        else:
            self.shipNum -= 1
            self.shipArray[size] -= 1
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
                self.check_destroyed(typeHit)
        else: #Have already fired here.
            print("Already fired here")

    def check_destroyed(self, typeHit):
        print("")
        if(any(typeHit in sublist for sublist in self.hidden) == False):
            for c in range(self.columns):
                for r in range(self.rows):
                    if(self.hidden[r][c] == typeHit + 10):
                        self.visible[r][c] = 3
            print("Destroyed a ship")

def StartGame(sizeX = 10, sizeY = 10, shipArray = [0, 1, 2, 1, 1]):
    playerBoard = Board(sizeX, sizeY, shipArray)
    computerBoard = Board(sizeX, sizeY, shipArray)
    ShipSetup()

def ShipSetup():
    print("Where do you want your first ship?")
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    message = r.recognize_google(audio)
    if "over" in r.recognize_google(audio):
        print("Gotcha!")
        print(message)
        type(message)
    else:
        print("I don't understand")
    print("Said nothing")

def PlayerTurn():
    pass

def ComputerTurn():
    pass

###
### Code for execution
###

StartGame()

"""
playerBoard = Board(10, 10, 5)
computerBoard = Board(10, 6, 5)

playerBoard.add_ship(5, 5, 1, 0, 3)
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

"""
# Prevent game from closing.
input("Exit Game?")
