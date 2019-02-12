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

alphabet = ["a","b","c","d","e","g","h","i","j","k"]

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

    def check_ship(self, x, y, dirX, dirY, size):
        if(x + dirX * size > self.columns):
            print("Out of bounds")
            return False
        if(y + dirY * size > self.rows):
            print("Out of bounds")
            return False
        for i in range(size):
            #If there is anything but water on any square, its not valid.
            if(self.hidden[x+i*dirX][y+i*dirY] != 0):
                return False
        return True

    def add_ship(self, x, y, dirX, dirY, size):
        for i in range(size):
            self.hidden[x-1+i*dirX][y-1-i*dirY] = self.shipNum
        self.shipNum -= 1
        self.shipArray[size] -= 1

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
    playerBoard.draw_hidden()
    playerBoard.draw_visible()
    ShipSetupPlayer(playerBoard)
    isRunning = True
    while(isRunning):
        PlayerTurn()
        ComputerTurn()
    print("Game Over")

def ShipSetupPlayer(playerBoard):
    for ships in range(playerBoard.shipNum):
        x = 1
        y = 1
        minSize = 1
        for i in range(playerBoard.shipNum):
            if(playerBoard.shipArray[i] != 0):
                minSize = i + 1
                break
        print(minSize)
        #INPUT: Coordinates
        while(True): #Loop until we break
            coordinates = input("Where do u want your ship?")
            #Reset if input doesnt have 2 characters
            if len(coordinates) != 2:
                continue
            temp = list(coordinates)
            x = temp[0].lower()
            y = temp[1].lower()

            if x in alphabet and y in alphabet:
                continue
            if IsNumber(x) == True and IsNumber(y) == True:
                continue
            #Make sure x is first
            try:
                int(y)
            except ValueError:
                x, y = y, x
            try:
                alphabet.index(x)
            except ValueError:
                continue
            #Make both integers for easier use in program
            x = alphabet.index(x) + 1 #Returns int
            y = int(y) #Returns int
            #Check if coordinate is empty
            if(playerBoard.hidden[x][y] != 0):
                continue
            #Reset if no direction is valid for this coordinate
            if(playerBoard.check_ship(x, y, 1, 0, minSize) == False):
                if(playerBoard.check_ship(x, y, -1, 0, minSize) == False):
                    if(playerBoard.check_ship(x, y, 0, 1, minSize) == False):
                        if(playerBoard.check_ship(x, y, 0, -1, minSize) == False):
                            continue
            break

        #INPUT: Direction
        while(True):
            direction = input("UP/DOWN/LEFT/RIGHT")
            if(direction.lower() in ["up", "u"]):
                dirX = 0
                dirY = 1
            elif(direction.lower() in ["down", "d"]):
                dirX = 0
                dirY = -1
            elif(direction.lower() in ["left", "l"]):
                dirX = -1
                dirY = 0
            elif(direction.lower() in ["right", "r"]):
                dirX = 1
                dirY = 0
            else:
                print("Input not valid")
                continue

            #Reset if minimum size of ship doesnt fit.
            if(playerBoard.check_ship(x, y, dirX, dirY, minSize) == False):
                continue
            break

        #INPUT: Size
        if(sum(playerBoard.shipArray) > 1):
            while(True):
                size = input("Size of ship")
                try:
                    size = int(size)
                except ValueError:
                    continue
                if(playerBoard.shipArray[size-1] == 0):
                    continue
                if(playerBoard.check_ship(x, y, dirX, dirY, size) == False):
                    continue
                break
        else:
            size = minSize

        print("Placed a ship at: ",x,y,dirX,dirY,size)
        playerBoard.add_ship(x, y, dirX, dirY, size)

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
