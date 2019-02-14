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
import random

###
### Variables and modules
###

# Declare and initiate PyGame Mixer.
mixer.init()

alphabet = ["a","b","c","d","e","g","h","i","j"]
numbers = ["1","2","3","4","5","6","7","8","9"]

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
        self.minSize = 0
        for i in range(len(shipArray)):
            if(shipArray[i] != 0):
                minSize = i + 1
                break

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
        x -= 1
        y -= 1
        lastX = x + dirX * (size-1)
        lastY = y + dirY * (size-1)
        if(0 > lastX or lastX > self.columns):
            print("Out of bounds")
            return False
        if(0 > lastY or lastY > self.rows):
            print("Out of bounds")
            return False
        for i in range(size):
            #If there is anything but water on any square, its not valid.
            if(self.hidden[x + i * dirX][y + i * dirY] != 0):
                print("Occupied")
                return False
        return True

    def add_ship(self, x, y, dirX, dirY, size):
        x -= 1
        y -= 1
        for i in range(size):
            self.hidden[x + i * dirX][y + i * dirY] = self.shipNum
        self.shipNum -= 1
        self.shipArray[size - 1] -= 1

    def fire(self, x, y):
        #Go from coordinate to index in array.
        x -= 1
        y -= 1
        target = self.visible[x][y]
        #Checks if there has already been fired at this square.
        if(target == 0): #Have not fired here before.
            hit = self.hidden[x][y]
            #Checks what was hit.
            if(hit == 0): #Water
                #Update information in array.
                self.visible[x][y] = 1
                print("Miss!")
            else: #Ship
                #Update both arrays
                self.visible[x][y] = 2
                typeHit = self.hidden[x][y]
                self.hidden[x][y] += 10
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

def GameLoop(sizeX = 9, sizeY = 9, array = [0, 1, 2, 1, 1], array1 = [0, 1, 2, 1, 1]):
    playerBoard = Board(sizeX, sizeY, array)
    computerBoard = Board(sizeX, sizeY, array1)
    playerBoard.draw_hidden()
    ShipSetup(playerBoard, True)
    ShipSetup(computerBoard, False)

    while(True):
        print("NEW TURN")
        print("")
        print("Player_hidden")
        playerBoard.draw_hidden()
        print("")
        print("Player_visible")
        playerBoard.draw_visible()
        print("")
        print("Computer_hidden")
        computerBoard.draw_hidden()
        print("")
        print("Computer_visible")
        computerBoard.draw_visible()
        PlayerTurn()
        ComputerTurn()
        #Infinite loop right now
        if(input("break?") == "y"):
            break
    print("Game Over")

def ShipSetup(selectedB, isPlayer):
    for ships in range(selectedB.shipNum):
        x = 1
        y = 1
        for i in range(len(selectedB.shipArray)):
            if(selectedB.shipArray[i] != 0):
                selectedB.minSize = i + 1
                break

        #INPUT: Coordinates
        x,y = SetCoords(selectedB, isPlayer, minSize)

        #INPUT: Direction
        dirX, dirY = SetDirection(selectedB, isPlayer, x, y)

        #INPUT: Size
        size = SetSize(selectedB, isPlayer, x, y, dirX, dirY)

        print("")
        selectedB.add_ship(x, y, dirX, dirY, size)
        selectedB.draw_hidden()
        print("shipArray: ", selectedB.shipArray)
        print("Placed a ship at: ", x, y, dirX, dirY, size)

    print("Deployed ships")



def PlayerTurn():
    pass

def ComputerTurn():
    pass

def SetCoords(selectedB, isPlayer, minSize):
    x = 1
    y = 1
    #INPUT: Coordinates.
    while(True): #Used as goto with continue keyword.
        if(isPlayer):
            coordinates = input("Where do u want your ship?")
        else:
            x = random.choice(alphabet)
            y = str(random.randint(1, 9))
            coordinates = x + y

        #Reset if input doesnt have 2 characters
        if len(coordinates) != 2:
            continue
        temp = list(coordinates)
        x = temp[0].lower()
        y = temp[1].lower()
        if x not in alphabet and x not in numbers:
            continue
        if y not in alphabet and y not in numbers:
            continue
        if x in alphabet and y in alphabet:
            continue
        if x in numbers and y in numbers:
            continue

        #Make sure x is first
        try:
            int(y)
        except ValueError:
            x, y = y, x

        #Make both integers for easier use in program
        x = alphabet.index(x) + 1 #Returns int
        y = int(y) #Returns int

        #Check if coordinate is empty
        if(selectedB.hidden[x-1][y-1] != 0):
            continue
        #Reset if no direction is valid for this coordinate
        if(selectedB.check_ship(x, y, 1, 0, minSize) == False):
            if(selectedB.check_ship(x, y, -1, 0, minSize) == False):
                if(selectedB.check_ship(x, y, 0, 1, minSize) == False):
                    if(selectedB.check_ship(x, y, 0, -1, minSize) == False):
                        continue
        break
    return x, y

def SetDirection(selectedB, isPlayer, x, y):
    while(True):
        if(isPlayer):
            direction = input("UP/DOWN/LEFT/RIGHT")
        else:
            direction = random.choice(["up","down","left","right"])

        if(direction.lower() in ["up", "u"]):
            dirX = 0
            dirY = -1
        elif(direction.lower() in ["down", "d"]):
            dirX = 0
            dirY = 1
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
        if(selectedB.check_ship(x, y, dirX, dirY, selectedB.minSize) == False):
            continue
        break
    return dirX, dirY

def SetSize(selectedB, isPlayer, x, y, dirX, dirY):
    if(sum(selectedB.shipArray) > 1):
        while(True):
            if(isPlayer):
                size = input("Size of ship")
            else:
                size = str(random.randint(1,len(selectedB.shipArray)+1))
                print("Size: ", size)

            try:
                size = int(size)
            except ValueError:
                continue
            try:
                selectedB.shipArray[size - 1]
            except IndexError:
                continue
            if(selectedB.shipArray[size - 1] == 0):
                continue
            if(selectedB.check_ship(x, y, dirX, dirY, selectedB.minSize) == False):
                continue
            break
    else:
        print("only one size")
        size = selectedB.minSize

    return size

###
### Code for execution
###

GameLoop()

# Prevent game from closing.
input("Exit Game?")
