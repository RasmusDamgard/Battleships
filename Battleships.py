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
import copy
mixer.init()

#Global constants. Read-only or deepcopied for use.
alphabet = ["a","b","c","d","e","f","g","h","i"]
numbers = ["1","2","3","4","5","6","7","8","9"]
shipArray = [0, 0, 0, 0, 1]
gridX = 9
gridY = 9

#Parameter object that stores all needed information about a ships placement
class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dirX = 0
        self.dirY = 0
        self.size = 0

###
### Start of Board class
###

#The class that controls a board. Two of these are instantiated.
class Board:
    #Constructor function that calculates and stores variables on instantiation
    def __init__(self, isPlayer):
        #Create two identical empty two-dimensional array.
        #These will be refered to as "the grid"
        self.visible = [[0 for rows in range(gridY)] for cols in range(gridX)]
        self.hidden = [[0 for rows in range(gridY)] for cols in range(gridX)]
        #Store the array of ships aswell as a counter of ships.
        self.shipArray = copy.deepcopy(shipArray)
        self.shipNum = sum(self.shipArray)
        #Store the number of total ships (constant), used for gameover condition
        self.shipNumMax = self.shipNum
        #The smallest ship in shipArray, is calculated when needed
        self.minSize = 1
        #Variable for AI, saves coordinate of last hit ship
        self.lastHit = []
        #Boolean for determining if board belongs to player or computer
        self.isPlayer = isPlayer
        self.shipParams = Ship()

    #These two functions draw the grid. Only used for developing/debugging.
    def draw_visible(self):
        for r in range(gridY):
            for c in range(gridX):
                print(self.visible[c][r], end=" ")
            print(" ")

    def draw_hidden(self):
        for r in range(gridY):
            for c in range(gridX):
                print(self.hidden[c][r], end=" ")
            print(" ")

    #Checks if a ship could be placed with given parameters
    #Returns True if a ship can be placed, False if it cant.
    def check_ship(self, ship: Ship, isMute: bool):
        #Starts at one end of a ship and calculates where the far end is
        lastX = ship.x + ship.dirX * (ship.size - 1)
        lastY = ship.y + ship.dirY * (ship.size - 1)
        #Checks if the end of the ship is larger or smaller than number of cols
        if(0 > lastX or lastX > gridX -1):
            if(isMute == False):
                PlayAudio("sfx_error")
                PlayAudio("i_out_of_bounds")
            return False

        #Exact same procedure for y-coordinate and rows
        if(0 > lastY or lastY > gridY -1):
            if(isMute == False):
                PlayAudio("sfx_error")
                PlayAudio("i_out_of_bounds")
            return False

        #Iterates through all the squares that the ship goes through
        for i in range(ship.size):
            #If there is anything BUT water on any square, its not valid.
            if(self.hidden[ship.x + ship.dirX * i][ship.y + ship.dirY * i] != 0):
                if(isMute == False):
                    PlayAudio("sfx_error")
                    PlayAudio("i_occupied")
                return False
        return True

    #Adds a ship to the grid based on a given Ship object
    #This function should only be called after check_ship() to avoid errors
    def add_ship(self, ship: Ship):
        #Iterate through all the squares that the ship goes through
        for i in range(ship.size):
            x = i * ship.dirX + ship.x
            y = i * ship.dirY + ship.y
            #Change information in the array to reflect the ship ID
            #Ship ID is equal to shipNum at this moment in time
            self.hidden[x][y] = self.shipNum
        #Reduce shipNum and thus the ship ID for the next ship
        self.shipNum -= 1
        #Remove the used ship from shipArray
        self.shipArray[ship.size - 1] -= 1

    #Checks if all squares of a ship has been hit, rendering the ship destroyed
    #Doesnt return anything, handles what needs to be handled internally
    def check_destroyed(self, shipID: int):
        #Checks if there exists a ship with the given shipID anywhere in grid
        #If not, its because the ship has been destroyed
        if(any(shipID in sublist for sublist in self.hidden) == False):
            #For AI purposes, change grid to reflect the ship is destroyed
            for c in range(gridX):
                for r in range(gridY):
                    if(self.hidden[r][c] == shipID + 10):
                        self.visible[r][c] = 3

            #Give sound feedback depending on whose board got hit
            if(self.isPlayer):
                PlayAudio("sfx_destroyed")
                PlayAudio("i_allied_ship_destroyed")
                #Clear AI memory
                self.lastHit.clear()
            else:
                PlayAudio("sfx_destroyed")
                PlayAudio("i_enemy_ship_destroyed")


    #Checks if all ships have been removed from the grid
    #Returns True if game is over, False if game is still going on
    def check_game_over(self):
        #For each ship ID
        for i in range (1, self.shipNumMax + 1):
            #Iterate through the grid and return False if shipID is found
            if(any(i in sublist for sublist in self.hidden) == True):
                return False
        #If nothing was found, return True (there are no ships left on grid)
        return True

    #Handles the placement of ships, has no return values or parameters
    def ship_setup(self):
        for ships in range(self.shipNum):
            #If its a player, inform them what ships they have left
            if (self.isPlayer):
                for i in range(len(self.shipArray)):
                    if (self.shipArray[i] == 0):
                        continue
                    PlayAudio("i_size_ava")
                    #PlayAudio(str(i+1))

            #Calculate minSize by iterating through shipArray
            for i in range(len(self.shipArray)):
                if(self.shipArray[i] != 0):
                    self.minSize = i + 1
                    break

            #Reset ship parameter object
            self.shipParams.size = self.minSize
            self.shipParams.x = 0
            self.shipParams.y = 0
            self.shipParams.dirX = 0
            self.shipParams.dirY = 0

            #Functions that determines and sets values for ship placement
            self.set_coords() #Determines x and y
            self.set_direction() #Determines dirX and dirY
            self.set_size()

            #Place the ship at given values.
            self.add_ship(self.shipParams)

            #Audio feedback for player
            if(self.isPlayer):
                PlayAudio("i_deploy")
                PlayAudio(alphabet[self.shipParams.x])
                PlayAudio(numbers[self.shipParams.y])
                PlayAudio("i_going")
                if(self.shipParams.dirX > 0):
                    PlayAudio("i_right")
                elif(self.shipParams.dirX < 0):
                    PlayAudio("i_left")
                elif(self.shipParams.dirY > 0):
                    PlayAudio("i_down")
                elif(self.shipParams.dirY < 0):
                    PlayAudio("i_up")
                PlayAudio("i_size")
                PlayAudio(str(self.shipParams.size))
        if(self.isPlayer):
            PlayAudio("i_all_ships_deploy")

    def set_coords(self):
        #isPlayer boolean determines what while loop to go into
        while(self.isPlayer): #Used as GOTO-statement with continue keyword
            #Ask for coordinates, allow user to input before message is over
            PlayAudio("q_coordinates", False)
            strCoords = input("Coordinates?")

            #Check if the inputted coordinates are valid
            if(CheckCoords(strCoords, True) == False):
                continue

            #Convert the string input into x and y integers
            x, y = ConvertCoords(strCoords)

            #Check if coordinate is empty
            if(self.hidden[x][y] != 0):
                #Position is not valid, a ship already occupies the spot
                PlayAudio("sfx_error")
                PlayAudio("i_occupied")
                continue

            self.shipParams.x = x
            self.shipParams.y = y
            ship1 = copy.deepcopy(self.shipParams)
            ship1.dirX = 1
            ship2 = copy.deepcopy(self.shipParams)
            ship2.dirX = -1
            ship3 = copy.deepcopy(self.shipParams)
            ship3.dirY = 1
            ship4 = copy.deepcopy(self.shipParams)
            ship4.dirY = -1

            print(ship1,ship2,ship3,ship4)
            #Reset if no direction is valid for this coordinate and minSize
            if(
            self.check_ship(ship1, True) == False and
            self.check_ship(ship2, True) == False and
            self.check_ship(ship3, True) == False and
            self.check_ship(ship4, True) == False):
            #Audio feedback should only be given if all directions are blocked
                PlayAudio("sfx_error")
                PlayAudio("i_no_space")
                continue

            #Inform player what coordinates they chose
            PlayAudio("sfx_accept")
            PlayAudio("i_selected")
            PlayAudio(alphabet[x])
            PlayAudio(numbers[y])

            #Break out of loop and end function
            break

        #A non-player board does almost the same, but with no audio feedback
        while(not self.isPlayer):
            strX = random.choice(alphabet)
            strY = random.choice(numbers)
            coordinates = strX + strY

            if(CheckCoords(coordinates, True) == False):
                continue

            x, y = ConvertCoords(coordinates)

            if(self.hidden[x][y] != 0):
                continue

            self.shipParams.x = x
            self.shipParams.y = y
            ship1 = copy.deepcopy(self.shipParams)
            ship1.dirX = 1
            ship2 = copy.deepcopy(self.shipParams)
            ship2.dirX = -1
            ship3 = copy.deepcopy(self.shipParams)
            ship3.dirY = 1
            ship4 = copy.deepcopy(self.shipParams)
            ship4.dirY = -1

            if(
            self.check_ship(ship1, True) == False and
            self.check_ship(ship2, True) == False and
            self.check_ship(ship3, True) == False and
            self.check_ship(ship4, True) == False):
                continue

            break

    def set_direction(self):
        while(self.isPlayer):
            PlayAudio("q_direction", False)
            strDirection = input("Direction?")

            #Parse input
            if(strDirection.lower() in ["up", "u"]):
                self.shipParams.dirY = -1
                strDirection = "up"
            elif(strDirection.lower() in ["down", "d"]):
                self.shipParams.dirY = 1
                strDirection = "down"
            elif(strDirection.lower() in ["left", "l"]):
                self.shipParams.dirX = -1
                strDirection = "left"
            elif(strDirection.lower() in ["right", "r"]):
                self.shipParams.dirX = 1
                strDirection = "right"
            else:
                #If input could not be parsed, it must be invalid
                PlayAudio("sfx_error")
                PlayAudio("i_invalid")
                continue

            #Reset if minimum size of ship doesnt fit.
            if(self.check_ship(self.shipParams, False) == False):
                #Sound feedback comes from check_ship()
                continue

            PlayAudio("sfx_accept")
            PlayAudio("i_selected")
            PlayAudio("i_" + strDirection)

            break

        while(not self.isPlayer):
            strDirection = random.choice(["up","down","left","right"])

            if(strDirection.lower() in ["up"]):
                self.shipParams.dirY = 1
            elif(strDirection.lower() in ["down"]):
                self.shipParams.dirY = -1
            elif(strDirection.lower() in ["left"]):
                self.shipParams.dirX = -1
            elif(strDirection.lower() in ["right"]):
                self.shipParams.dirX = 1

            if(self.check_ship(self.shipParams, True) == False):
                continue

            break

    def set_size(self):
        while(self.isPlayer):
            PlayAudio("q_size", False)
            strSize = input("Size of ship")

            #Is input an integer? Then parse it
            try:
                size = int(strSize)
            except ValueError:
                #If not, restart while loop
                PlayAudio("sfx_error")
                PlayAudio("i_invalid")
                continue
            self.shipParams.size = int(strSize)

            #Does a ship of specified size exist
            try:
                self.shipArray[self.shipParams.size - 1]
            except IndexError:
                PlayAudio("sfx_error")
                PlayAudio("i_no_exist_ship")
                continue

            #Does player have any ships of this size left?
            if(self.shipArray[self.shipParams.size - 1] == 0):
                PlayAudio("sfx_error")
                PlayAudio("i_no_ships_size")
                PlayAudio(strSize)
                continue

            #Can a ship be placed with that size?
            if(self.check_ship(self.shipParams, False) == False):
                PlayAudio("i_choose_smaller")
                continue

            PlayAudio("sfx_accept")
            PlayAudio("i_selected")
            PlayAudio(strSize)

            break

        while(not self.isPlayer):
            strSize = str(random.randint(1,len(self.shipArray)))
            try:
                size = int(strSize)
            except ValueError:
                continue
            self.shipParams.size = int(strSize)
            try:
                self.shipArray[self.shipParams.size - 1]
            except IndexError:
                continue
            if(self.shipArray[self.shipParams.size - 1] == 0):
                continue
            if(self.check_ship(self.shipParams, True) == False):
                continue

            break

###
### End of Board class
###

#Main function that calls all other functions
def GameLoop():
    #TODO: Make automatic
    PlayAudio("q_tutorial", False)
    tutPlay = input("Do u want to hear a tutorial on how to play?")
    if (tutPlay == "y"):
        PlayAudio("i_tutorial")

    #Functions that only need to be called once
    playerBoard = Board(True)
    computerBoard = Board(False)
    playerBoard.ship_setup()
    computerBoard.ship_setup()
    computerBoard.draw_hidden()
    #The loop in which the game is played, only breaks on game over.
    while(True):
        #Players turn, they fire at the opponents board
        FireAt(computerBoard, True)

        #Computerturn
        FireAt(playerBoard, False)

        #Check if game is over and determine winner. Then break out of loop.
        if(computerBoard.check_game_over() == True):
            if(playerBoard.check_game_over() == True):
                PlayAudio("i_tie")
            else:
                PlayAudio("i_win")
            break
        elif(playerBoard.check_game_over() == True):
            PlayAudio("i_loss")
            break

#TODO: More commenting
def FireAt(selectedB, isPlayer):
    x = 0
    y = 0
    limiter = 0
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
            selectedB.check_destroyed(shipID)
        #Break out of loop
        break

    while(isPlayer == False):
        limiter += 1
        #If computer hit something last turn, initiate AI algorhytm
        if(selectedB.lastHit != [] and limiter < 25):
            print("This hap 1")
            print(limiter)
            print(selectedB.lastHit)
            #Create shorthand variable
            r = selectedB.lastHit
            #If we hit multiple times, we can determine direction
            if(len(r)>2):
                print("tjos hap 2")
                #If x is same for both hits, ship must be differing on y
                if(r[0]==r[2]):
                    #x should be the same value
                    x = r[0]
                    #but y should be either one below or one above lasthits
                    t = r[1]-r[3]
                    y = int(r[1] + t - t*random.randint(0,1)*(len(r)/2 + 1))
                #Same method, but reverse
                if(r[1]==r[3]):
                    t = r[0]-r[2]
                    x = int(r[0] + t - t*random.randint(0,1)*(len(r)/2 + 1))
                    y = r[1]
            #We hit once, ship must be in one of the 4 adjacent squares
            else:
                print("this 3")
                #Same coordinates as lasthit, but add or remove one at random
                temp = random.randint(0,3)
                x = r[0]
                y = r[1]
                if(temp == 0):
                    x += 1
                if(temp == 1):
                    x -= 1
                if(temp == 2):
                    y += 1
                if(temp == 3):
                    y -= 1
            if(x<0 or y<0):
                continue
        else: #If nothing was hit last turn, select completely random
            selectedB.lastHit.clear()
            print("This 4 works")
            x = random.choice(alphabet)
            y = random.choice(numbers)
            coordinates = x + y
            if(CheckCoords(coordinates, False) == False):
                print("oops")
                continue
            x,y = ConvertCoords(coordinates)
        print("x:",x,";y:",y)
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
            PlayAudio("sfx_miss")
            PlayAudio("i_enemy_miss")
        else: #Hit ship.
            #Update both arrays
            selectedB.visible[x][y] = 2
            shipID = selectedB.hidden[x][y]
            selectedB.hidden[x][y] += 10
            PlayAudio("sfx_hit")
            PlayAudio("i_enemy_hit")
            #Check if a ship was destroyed
            selectedB.lastHit.append(x)
            selectedB.lastHit.append(y)
            selectedB.check_destroyed(shipID)
            print("They hit us")
        #Break out of loop
        break

def CheckCoords(coordinates, isMute):
    #Reset if input doesnt have 2 characters
    if len(coordinates) != 2:
        if(not isMute):
            PlayAudio("sfx_error")
            PlayAudio("i_invalid")
        return False

    temp = list(coordinates)
    x = temp[0].lower()
    y = temp[1].lower()

    if x not in alphabet and x not in numbers:
        if(isPlayer):
            PlayAudio("sfx_error")
            PlayAudio("i_invalid")
        return False
    if y not in alphabet and y not in numbers:
        if(isPlayer):
            PlayAudio("sfx_error")
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

#Takes one parameter of type string.
#Returns the x and y values it represents
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
input("Exit Game?") #Game will close when enter is pressed
