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
from pygame import mixer

###
### Variables and modules
###

# Declare and initiate PyGame Mixer.
mixer.init()

alphabet = ["a","b","c","d","e","g","h","i","j","k","l","m","n","o"]

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

def GameLoop(sizeX = 10, sizeY = 10, shipArray = [0, 1, 2, 1, 1]):
    playerBoard = Board(sizeX, sizeY, shipArray)
    computerBoard = Board(sizeX, sizeY, shipArray)
    ShipSetupPlayer(playerBoard)
    isRunning = True
    while(isRunning):
        PlayerTurn()
        ComputerTurn()
    print("Game is over")

def ShipSetupPlayer(playerBoard):
    for i in range(playerBoard.shipNum):
        isValid = False
        x = 1
        y = 1
        while(isValid == False):
            coords = input("Where do u want your ship?")
            if len(coords) != 2:
                isValid = False
                continue

            coordsSplit = list(coords)
            x = coordsSplit[0].lower()
            y = coordsSplit[1].lower()

            print("Had two letters:", x, y)

            
            if x in alphabet or y in alphabet:
                if IsNumber(x) == True or IsNumber(y) == True:
                    try:
                        int(y)    
                    except ValueError:
                        x, y = y, x   
                    x = alphabet.index(x)
                    y = int(y)
                    print("Placed a ship")
                    break
                print("Was in the alphabet")
            continue

        #Add ship
        
    print("Deployed ships")



def PlayerTurn():
    pass

def ComputerTurn():
    pass

def IsNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

###
### Code for execution
###

GameLoop()

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
