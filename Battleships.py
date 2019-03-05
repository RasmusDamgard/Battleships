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
import wave
import time

###
### Variables and modules
###

# Declare and initiate PyGame Mixer.
mixer.init()

#Global constants
alphabet = ["a","b","c","d","e","f","g","h","i"]
numbers = ["1","2","3","4","5","6","7","8","9"]

###audioFile = alphabet[x]+".wav"

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
        self.shipNumMax = self.shipNum
        self.minSize = 1
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

    def check_ship(self, x, y, dirX, dirY, size, isPlayer):
        lastX = x + dirX * (size - 1)
        lastY = y + dirY * (size - 1)
        if(0 > lastX or lastX > self.columns -1):
            if(isPlayer): #Player does
                print("Your ship: Out of bounds")
                PlayAudio("i_out_of_bounds")
                #If it isnt the player, theres no need to output feedback.
            return False
        if(0 > lastY or lastY > self.rows -1):
            if(isPlayer): #Player does
                print("Your ship: Out of bounds")
                PlayAudio("i_out_of_bounds")
                #If it isnt the player, theres no need to output feedback.
            return False
        for i in range(size):
            #If there is anything but water on any square, its not valid.
            if(self.hidden[x + dirX * i][y + dirY * i] != 0):
                if(isPlayer): #Player does
                    print("Your ship: Spot is occupied")
                    PlayAudio("i_occupied")
                    #If it isnt the player, theres no need to output feedback.
                return False
        return True

    def add_ship(self, x, y, dirX, dirY, size):
        for i in range(size):
            self.hidden[x + i * dirX][y + i * dirY] = self.shipNum
        self.shipNum -= 1
        self.shipArray[size - 1] -= 1

    def check_destroyed(self, typeHit, isPlayer):
        if(any(typeHit in sublist for sublist in self.hidden) == False):
            for c in range(self.columns):
                for r in range(self.rows):
                    if(self.hidden[r][c] == typeHit + 10):
                        self.visible[r][c] = 3
            if(isPlayer):
                print("You have destroyed a ship")
                PlayAudio("i_destroyed_ship")
            elif(isPlayer == False):
                print("Enemy has destroyed one of your ships")
                #TODO: "Enemy destroyed ship"

    def check_game_over(self):
        isGameOver = True
        for i in range (1, self.shipNumMax + 1):
            if(any(i in sublist for sublist in self.hidden) == True):
                isGameOver = False
        return isGameOver

def GameLoop(sizeX = 9, sizeY = 9, array = [0, 1, 0, 0, 1], array1 = [0, 1, 0, 0, 1]):
    playerBoard = Board(sizeX, sizeY, array)
    computerBoard = Board(sizeX, sizeY, array1)
    playerBoard.draw_hidden()
    ShipSetup(playerBoard, True)
    ShipSetup(computerBoard, False)

    while(True):
        print("NEW TURN")
        print("")
        print("Computer_hidden")
        computerBoard.draw_hidden()
        print("")
        print("Player_visible")
        playerBoard.draw_visible()
        print("")
        print("Player_hidden")
        playerBoard.draw_hidden()
        print("")
        print("Computer_visible")
        computerBoard.draw_visible()
        print("")


        #Playerturn
        TakeTurn(computerBoard, True)
        #Computerturn
        TakeTurn(playerBoard, False)

        #Check if game is over and determine winner.
        if(computerBoard.check_game_over() == True):
            if(playerBoard.check_game_over() == True):
                print("Game Over: It's a tie!")
            else:
                print("Game Over: You won!")
            break
        elif(playerBoard.check_game_over() == True):
            print("Game Over: You lost!")
            break

def ShipSetup(selectedB, isPlayer):
    for ships in range(selectedB.shipNum):
        x = 0
        y = 0
        minSize = 1
        for i in range(len(selectedB.shipArray)):
            if(selectedB.shipArray[i] != 0):
                selectedB.minSize = i + 1
                break
        #INPUT: Coordinates
        x,y = SetCoords(selectedB, isPlayer)
        #INPUT: Direction
        dirX, dirY = SetDirection(selectedB, isPlayer, x, y)
        #INPUT: Size
        size = SetSize(selectedB, isPlayer, x, y, dirX, dirY)
        print("")
        selectedB.add_ship(x, y, dirX, dirY, size)
        selectedB.draw_hidden()
        if(isPlayer):
            print("Deployed a ship, at: ", x, y, dirX, dirY, size)
            PlayAudio("i_deploy")
            PlayAudio(alphabet[x])
            PlayAudio(numbers[y])
            PlayAudio("i_going")
            if(dirX > 0):
                PlayAudio("i_right")
            elif(dirX < 0):
                PlayAudio("i_left")
            elif(dirY > 0):
                PlayAudio("i_down")
            elif(dirY < 0):
                PlayAudio("i_up")
            PlayAudio("i_size")
            PlayAudio(str(size))
    if(isPlayer):
        print("Deployed ships")
        #TODO: "ALL ships deployed"

def TakeTurn(selectedB, isPlayer):
    x = 0
    y = 0
    while(isPlayer):
        #Voicefeedback: Prompt fire coords
        #TODO: "Where to fire"
        coordinates = input("Where do you want to fire?")

        if(CheckCoords(coordinates, isPlayer) == False):
            #Sound feedback comes from CheckCoords
            continue

        x,y = ConvertCoords(coordinates)

        if(selectedB.visible[x][y] > 0):
            print("Not valid: You have already fired, at")
            PlayAudio("i_already_fired")
            PlayAudio(alphabet[x])
            PlayAudio(numbers[y])
            continue

        #We know that firing coordinates are valid
        print("You fired at: ", x, "; ", y)
        #TODO: "You selected, "
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])

        #Checks what was hit.
        if(selectedB.hidden[x][y] == 0): #Hit water.
            #Update information in array.
            selectedB.visible[x][y] = 1
            print("You missed!")
            PlayAudio("i_miss")
        else: #Hit ship.
            #Update both arrays
            selectedB.visible[x][y] = 2
            typeHit = selectedB.hidden[x][y]
            selectedB.hidden[x][y] += 10
            print("You hit!")
            #TODO: change "i_hit" to not mention coords
            PlayAudio("i_hit")
            #Check if a ship was destroyed
            selectedB.check_destroyed(typeHit, True)
        #Break out of loop
        break

    while(isPlayer == False):
        x = random.choice(alphabet)
        y = random.choice(numbers)
        coordinates = x + y

        #Check if input is valid
        if(CheckCoords(coordinates, False) == False):
            continue

        x,y = ConvertCoords(coordinates)

        if(selectedB.visible[x][y] > 0):
            #Already fired here
            continue

        #We know that firing coordinates are valid
        print("Your enemy fired at:")
        #TODO: "Enemy fired, at"
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])

        #Checks what was hit.
        if(selectedB.hidden[x][y] == 0): #Hit water.
            #Update information in array.
            selectedB.visible[x][y] = 1
            print("Enemy missed your ships!")
            #TODO: "Enemy missed ship"
        else: #Hit ship.
            #Update both arrays
            selectedB.visible[x][y] = 2
            typeHit = selectedB.hidden[x][y]
            selectedB.hidden[x][y] += 10
            print("Enemy hit your ships!")
            #TODO: "Enemy hit ship"
            #Check if a ship was destroyed
            selectedB.check_destroyed(typeHit, False)
        #Break out of loop
        break

def SetCoords(selectedB, isPlayer):
    x = 0
    y = 0
    #INPUT: Coordinates.
    while(isPlayer): #Used as goto with continue keyword.
        PlayAudio("q_next_ship", False)
        #TODO: Change next/first ship into universal audio
        coordinates = input("Where do you want your ship?")

        #Reset if input doesnt have 2 characters
        if(CheckCoords(coordinates, isPlayer) == False):
            continue

        x, y = ConvertCoords(coordinates)
        #TODO: "You selected ,"
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])

        #Check if coordinate is empty
        if(selectedB.hidden[x][y] != 0):
            print("Not Valid: You already have a ship here.")
            PlayAudio("i_occupied")
            continue
        #Reset if no direction is valid for this coordinate
        if(selectedB.check_ship(x, y, 1, 0, selectedB.minSize, False) == False):
            if(selectedB.check_ship(x, y, -1, 0, selectedB.minSize, False) == False):
                if(selectedB.check_ship(x, y, 0, 1, selectedB.minSize, False) == False):
                    if(selectedB.check_ship(x, y, 0, -1, selectedB.minSize, False) == False):
                        print("Not Valid: Not enouogh space for a ship.")
                        #TODO: "No space for ship"
                        continue
        break

    while(isPlayer == False):
        x = random.choice(alphabet)
        y = random.choice(numbers)
        coordinates = x + y
        #Reset if input doesnt have 2 characters
        if(CheckCoords(coordinates, False) == False):
            continue

        x, y = ConvertCoords(coordinates)

        #Check if coordinate is empty
        if(selectedB.hidden[x][y] != 0):
            continue
        #Reset if no direction is valid for this coordinate
        if(selectedB.check_ship(x, y, 1, 0, selectedB.minSize, False) == False):
            if(selectedB.check_ship(x, y, -1, 0, selectedB.minSize, False) == False):
                if(selectedB.check_ship(x, y, 0, 1, selectedB.minSize, False) == False):
                    if(selectedB.check_ship(x, y, 0, -1, selectedB.minSize, False) == False):
                        continue
        break
    return x, y

def SetDirection(selectedB, isPlayer, x, y):
    while(isPlayer):
        PlayAudio("q_direction", False)
        direction = input("UP/DOWN/LEFT/RIGHT")
        if(direction.lower() in ["up", "u"]):
            dirX = 0
            dirY = -1
            #TODO: "You selected,
            PlayAudio("i_up")
        elif(direction.lower() in ["down", "d"]):
            dirX = 0
            dirY = 1
            #TODO: "You selected,
            PlayAudio("i_down")
        elif(direction.lower() in ["left", "l"]):
            dirX = -1
            dirY = 0
            #TODO: "You selected,
            PlayAudio("i_left")
        elif(direction.lower() in ["right", "r"]):
            dirX = 1
            dirY = 0
            #TODO: "You selected,
            PlayAudio("i_right")
        else:
            print("Input not valid")
            #TODO: Invalid input
            continue

        #Reset if minimum size of ship doesnt fit.
        if(selectedB.check_ship(x, y, dirX, dirY, selectedB.minSize, True) == False):
            #Sound feedback comes from check_ship
            continue
        break

    while(isPlayer == False):
        direction = random.choice(["up","down","left","right"])
        if(direction.lower() in ["up"]):
            dirX = 0
            dirY = -1
        elif(direction.lower() in ["down"]):
            dirX = 0
            dirY = 1
        elif(direction.lower() in ["left"]):
            dirX = -1
            dirY = 0
        elif(direction.lower() in ["right"]):
            dirX = 1
            dirY = 0

        #Reset if minimum size of ship doesnt fit.
        if(selectedB.check_ship(x, y, dirX, dirY, selectedB.minSize, False) == False):
            continue
        break

    return dirX, dirY

def SetSize(selectedB, isPlayer, x, y, dirX, dirY):
    while(isPlayer):
        PlayAudio("q_size", False)
        size = input("Size of ship")
        try:
            size = int(size)
        except ValueError:
            print("Input not valid")
            #TODO: "invalid"
            continue
        #Does a ship of specified size exist (is it below 5 in size)
        try:
            selectedB.shipArray[size - 1]
        except IndexError:
            print("Not valid: Ship of this size does not exist")
            #TODO: "A ship of this size does not exist" (NO MENTION OF ACTUAL SIZE)
            #PlayAudio("")
            continue
        if(selectedB.shipArray[size - 1] == 0):
            print("Not valid: No ships of this size")
            PlayAudio("i_no_ships_size")
            PlayAudio(str(size))
            continue
        if(selectedB.check_ship(x, y, dirX, dirY, size, True) == False):
            print("Not Valid: Choose a smaller size")
            #TODO: Choose a smaller size
            continue
        break

    while(isPlayer == False):
        size = str(random.randint(1,len(selectedB.shipArray)))
        try:
            size = int(size)
        except ValueError:
            continue
        #Does a ship of specified size exist (is it below 5 in size)
        try:
            selectedB.shipArray[size - 1]
        except IndexError:
            continue
        if(selectedB.shipArray[size - 1] == 0):
            continue
        if(selectedB.check_ship(x, y, dirX, dirY, size, False) == False):
            continue
        break

    return size

def CheckCoords(coordinates, isPlayer):
    #Reset if input doesnt have 2 characters
    if len(coordinates) > 2:
        if(isPlayer):
            print("Not valid: Too many characters in input")
            #TODO: "Too many characters"
        return False
    if len(coordinates) < 2:
        if(isPlayer):
            print("Not Valid: Too few characters in input")
            #TODO: "Too few characters"
        return False
    temp = list(coordinates)
    x = temp[0].lower()
    y = temp[1].lower()
    if x not in alphabet and x not in numbers:
        if(isPlayer):
            print("Not Valid: invalid characters")
            #TODO: "Invalid Input"
        return False
    if y not in alphabet and y not in numbers:
        if(isPlayer):
            print("Not Valid: invalid characters")
        return False
    if x in alphabet and y in alphabet:
        if(isPlayer):
            print("Not Valid: invalid characters")
        return False
    if x in numbers and y in numbers:
        if(isPlayer):
            print("Not Valid: invalid characters")
        return False

    return True

def ConvertCoords(coordinates):
    temp = list(coordinates)
    x = temp[0].lower()
    y = temp[1].lower()

    #Make sure x is first
    try:
        int(y)
    except ValueError:
        x, y = y, x

    #Make both integers for easier use in program
    x = alphabet.index(x) #Returns int
    y = numbers.index(y) #Returns int

    return x, y

def PlayAudio(fileName, sleep = True):
    path = "audio/" + fileName + ".wav"
    mixer.music.load(path)
    mixer.music.play()
    if(sleep):
        wr = wave.open(path, "r")
        frames = wr.getnframes()
        frameRate = wr.getframerate()
        duration = frames / frameRate
        time.sleep(duration)


#Start the game
GameLoop()

#Prevent game from closing instantly.
input("Exit Game?")
