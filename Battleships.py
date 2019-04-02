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
mixer.init()

#Global constants
alphabet = ["a","b","c","d","e","f","g","h","i"]
numbers = ["1","2","3","4","5","6","7","8","9"]

###
### Classes & Functions
###

#The class that controls a players board
class Board:
    #Constructor function that calculates and stores variables on instantiation
    def __init__(self, columns, rows, shipArray):
        #Create two identical empty two-dimensional array.
        #These will be refered to as "the grid"
        self.visible = [[0 for rows in range(rows)] for cols in range(columns)]
        self.hidden = [[0 for rows in range(rows)] for cols in range(columns)]
        #Store column and row information in this instance.
        self.columns = columns
        self.rows = rows
        #Store the array of ships aswell as a counter of ships.
        self.shipArray = shipArray
        self.shipNum = sum(self.shipArray)
        #Store the number of total ships (constant), used for gameover condition
        self.shipNumMax = self.shipNum
        #Calculate the smallest ship in shipArray
        self.minSize = 1
        for i in range(len(shipArray)):
            if(shipArray[i] != 0):
                minSize = i + 1
                break

    #These two functions draw the grid (two-dimensional array)
    #Only used for developing
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

    #Checks if a ship could be placed with given parameters
    #Returns True if a ship can be placed, False if it cant.
    #Parameter datatypes: (self, int, int, int, int, int, boolean)
    def check_ship(self, x, y, dirX, dirY, size, isPlayer):
        #Starts at one end of a ship and calculates where the other end is
        lastX = x + dirX * (size - 1)
        lastY = y + dirY * (size - 1)
        #Checks if the end of the ship is larger or smaller than
        if(0 > lastX or lastX > self.columns -1):
            #If a player does this, output audio feedback
            if(isPlayer):
                PlayAudio("sfx_error")
                PlayAudio("i_out_of_bounds")
            #If it isnt the player, we shouldnt output audio feedback
            #No matter if it is computer or player we want to return false
            return False

        #Exact same procedure for y-coordinate
        if(0 > lastY or lastY > self.rows -1):
            if(isPlayer):
                PlayAudio("sfx_error")
                PlayAudio("i_out_of_bounds")
            return False

        #Iterates through all the squares that the ship goes through
        for i in range(size):
            #If there is anything BUT water on any square, its not valid.
            if(self.hidden[x + dirX * i][y + dirY * i] != 0):
                if(isPlayer):
                    PlayAudio("sfx_error")
                    PlayAudio("i_occupied")
                return False
        return True

    #Adds a ship to the grid based on given parameters
    #This function should only be called after check_ship() to avoid errors
    #Parameter datatypes: (self, int, int, int, int, int)
    def add_ship(self, x, y, dirX, dirY, size):
        #Iterate through all the squares that the ship goes through
        for i in range(size):
            #Change information in the array to reflect the ship ID
            #Ship ID is equal to shipNum at this moment in time
            self.hidden[x + i * dirX][y + i * dirY] = self.shipNum
        #Reduce shipNum and thus the ship ID for the next ship
        self.shipNum -= 1
        #Remove the used ship from shipArray
        self.shipArray[size - 1] -= 1

    #Checks if all squares of a ship has been hit, rendering the ship destroyed
    #Doesnt return anything, handles what needs to be handled immediately
    #Paramter dataypes: (self, int, boolean)
    def check_destroyed(self, shipID, isPlayer):
        #Checks if there exists a ship with the given shipID anywhere in grid
        #If not, its because the ship has been destroyed
        if(any(shipID in sublist for sublist in self.hidden) == False):
            #Give sound feedback depending on whose board got hit
            if(isPlayer):
                PlayAudio("sfx_destroyed")
                PlayAudio("i_destroyed_ship")
            else:
                PlayAudio("sfx_destroyed")
                PlayAudio("i_enemy_destroyed")

    #Checks if all ships have been removed from the grid
    #Returns True if game is over, False if game is still going on.
    def check_game_over(self):
        #For each ship ID
        for i in range (1, self.shipNumMax + 1):
            #Iterate through the grid and return False if anything is found
            if(any(i in sublist for sublist in self.hidden) == True):
                return False
        #If nothing was found, return True
        return True

#Main function that calls all other functions
#TODO: MORE COMMENTING    ->
def GameLoop(sizeX = 9, sizeY = 9, array_player = [0, 1, 0, 0, 1], array_computer = [0, 1, 0, 0, 1]):
    PlayAudio("q_tutorial", False)
    tutPlay = input("Do u want to hear a tutorial on how to play?")
    if (tutPlay == "y"):
        PlayAudio("i_tutorial")
    playerBoard = Board(sizeX, sizeY, array_player)
    computerBoard = Board(sizeX, sizeY, array_computer)
    #playerBoard.draw_hidden()
    ShipSetup(playerBoard, True)
    ShipSetup(computerBoard, False)

    while(True):
        print("NEW TURN")
        #print("")
        #print("Computer_hidden")
        #computerBoard.draw_hidden()
        #print("")
        #print("Player_visible")
        #playerBoard.draw_visible()
        #print("")
        #print("Player_hidden")
        #playerBoard.draw_hidden()
        #print("")
        #print("Computer_visible")
        #computerBoard.draw_visible()
        print("")

        #Playerturn
        TakeTurn(computerBoard, True)
        #Computerturn
        TakeTurn(playerBoard, False)

        #Check if game is over and determine winner. Then break out of GameLoop()
        if(computerBoard.check_game_over() == True):
            if(playerBoard.check_game_over() == True):
                PlayAudio("i_tie")
                print("Game Over: It's a tie!")
            else:
                PlayAudio("i_win")
                print("Game Over: You won!")
            break
        elif(playerBoard.check_game_over() == True):
            PlayAudio("i_loss")
            print("Game Over: You lost!")
            break

def ShipSetup(selectedB, isPlayer):
    for ships in range(selectedB.shipNum):
        if (isPlayer):
            for i in range(len(selectedB.shipArray)):
                if (selectedB.shipArray[i] == 0):
                    continue
                PlayAudio("i_size_ava")
                PlayAudio(str(i+1))

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
            #print("Deployed a ship, at: ", x, y, dirX, dirY, size)
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
        #print("Deployed ships")
        PlayAudio("i_all_ships_deploy")

def TakeTurn(selectedB, isPlayer):
    x = 0
    y = 0
    while(isPlayer):
        #Voicefeedback: Prompt fire coords
        PlayAudio("q_fire")
        coordinates = input("Where do you want to fire?")

        if(CheckCoords(coordinates, isPlayer) == False):
            #Sound feedback comes from CheckCoords
            continue

        x,y = ConvertCoords(coordinates)

        if(selectedB.visible[x][y] > 0):
            PlayAudio("sfx_error")
            #print("Not valid: You have already fired, at")
            PlayAudio("i_already_fired")
            PlayAudio(alphabet[x])
            PlayAudio(numbers[y])
            continue

        #We know that firing coordinates are valid
        #print("You fired at: ", x, "; ", y)
        PlayAudio("sfx_accept")
        PlayAudio("i_selected")
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])
        PlayAudio("sfx_fire")

        #Checks what was hit.
        if(selectedB.hidden[x][y] == 0): #Hit water.
            #Update information in array.
            selectedB.visible[x][y] = 1
            #print("You missed!")
            PlayAudio("sfx_miss")
            PlayAudio("i_miss")
        else: #Hit ship.
            #Update both arrays
            selectedB.visible[x][y] = 2
            shipID = selectedB.hidden[x][y]
            selectedB.hidden[x][y] += 10
            #print("You hit!")
            PlayAudio("sfx_hit")
            PlayAudio("i_hit")
            #Check if a ship was destroyed
            selectedB.check_destroyed(shipID, True)
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
        PlayAudio("i_enemy_fire")
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])
        PlayAudio("sfx_fire")

        #Checks what was hit.
        if(selectedB.hidden[x][y] == 0): #Hit water.
            #Update information in array.
            selectedB.visible[x][y] = 1
            #print("Enemy missed your ships!")
            PlayAudio("sfx_miss")
            PlayAudio("i_enemy_miss")
        else: #Hit ship.
            #Update both arrays
            selectedB.visible[x][y] = 2
            shipID = selectedB.hidden[x][y]
            selectedB.hidden[x][y] += 10
            #print("Enemy hit your ships!")
            PlayAudio("sfx_hit")
            PlayAudio("i_enemy_hit")
            #Check if a ship was destroyed
            selectedB.check_destroyed(shipID, False)
        #Break out of loop
        break

def SetCoords(selectedB, isPlayer):
    x = 0
    y = 0
    #INPUT: Coordinates.
    while(isPlayer): #Used as goto with continue keyword.
        PlayAudio("q_coordinates", False)
        coordinates = input("Where do you want your ship?")

        if(CheckCoords(coordinates, isPlayer) == False):
            continue

        x, y = ConvertCoords(coordinates)

        #Check if coordinate is empty
        if(selectedB.hidden[x][y] != 0):
            PlayAudio("sfx_error")
            print("Not Valid: You already have a ship here.")
            PlayAudio("i_occupied")
            continue
        #Reset if no direction is valid for this coordinate
        if(selectedB.check_ship(x, y, 1, 0, selectedB.minSize, False) == False):
            if(selectedB.check_ship(x, y, -1, 0, selectedB.minSize, False) == False):
                if(selectedB.check_ship(x, y, 0, 1, selectedB.minSize, False) == False):
                    if(selectedB.check_ship(x, y, 0, -1, selectedB.minSize, False) == False):
                        PlayAudio("sfx_error")
                        print("Not Valid: Not enouogh space for a ship.")
                        PlayAudio("i_no_space")
                        continue
        PlayAudio("sfx_accept")
        PlayAudio("i_selected")
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])
        break

    while(isPlayer == False):
        x = random.choice(alphabet)
        y = random.choice(numbers)
        coordinates = x + y

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
            direction = "up"
        elif(direction.lower() in ["down", "d"]):
            dirX = 0
            dirY = 1
            direction = "down"
        elif(direction.lower() in ["left", "l"]):
            dirX = -1
            dirY = 0
            direction = "left"
        elif(direction.lower() in ["right", "r"]):
            dirX = 1
            dirY = 0
            direction = "right"
        else:
            PlayAudio("sfx_error")
            print("Input not valid")
            PlayAudio("i_invalid")
            continue

        #Reset if minimum size of ship doesnt fit.
        if(selectedB.check_ship(x, y, dirX, dirY, selectedB.minSize, True) == False):
            #Sound feedback comes from check_ship
            continue

        PlayAudio("sfx_accept")
        PlayAudio("i_selected")
        PlayAudio("i_"+direction)
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
            PlayAudio("sfx_error")
            print("Input not valid")
            PlayAudio("i_invalid")
            continue
        #Does a ship of specified size exist (is it below 5 in size)
        try:
            selectedB.shipArray[size - 1]
        except IndexError:
            PlayAudio("sfx_error")
            print("Not valid: Ship of this size does not exist")
            PlayAudio("i_no_exist_ship")
            #PlayAudio("")
            continue
        if(selectedB.shipArray[size - 1] == 0):
            PlayAudio("sfx_error")
            print("Not valid: No ships of this size")
            PlayAudio("i_no_ships_size")
            PlayAudio(str(size))
            continue
        if(selectedB.check_ship(x, y, dirX, dirY, size, True) == False):
            print("Not Valid: Choose a smaller size")
            PlayAudio("i_choose_smaller")
            continue
        PlayAudio("sfx_accept")
        PlayAudio("i_selected")
        PlayAudio(str(size))
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
            PlayAudio("sfx_error")
            print("Not valid: Too many characters in input")
            #TODO: "Too many characters"
            PlayAudio("i_invalid")
        return False
    if len(coordinates) < 2:
        if(isPlayer):
            PlayAudio("sfx_error")
            print("Not Valid: Too few characters in input")
            #TODO: "Too few characters"
            PlayAudio("i_invalid")
        return False
    temp = list(coordinates)
    x = temp[0].lower()
    y = temp[1].lower()
    if x not in alphabet and x not in numbers:
        if(isPlayer):
            PlayAudio("sfx_error")
            print("Not Valid: invalid characters")
            PlayAudio("i_invalid")
        return False
    if y not in alphabet and y not in numbers:
        if(isPlayer):
            PlayAudio("sfx_error")
            print("Not Valid: invalid characters")
            PlayAudio("i_invalid")
        return False
    if x in alphabet and y in alphabet:
        if(isPlayer):
            PlayAudio("sfx_error")
            print("Not Valid: invalid characters")
            PlayAudio("i_invalid")
        return False
    if x in numbers and y in numbers:
        if(isPlayer):
            PlayAudio("sfx_error")
            print("Not Valid: invalid characters")
            PlayAudio("i_invalid")
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


#Start the game by calling GameLoop() once
GameLoop()

#Prevent game from closing instantly after GameLoop() is over
input("Exit Game?")
