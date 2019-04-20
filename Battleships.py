# -----------------------------------------------------------------------------
# Name:        Battleships! - Audio-only edition
# Purpose:     To help blind people enjoy games
#
# Author:      Oliver Thejl Eriksen (Olipus)
#              Rasmus Damgaard-Iversen (Mastercoder27)
#
# Created:     30-01-2019
# Copyright:   (c) 2019, Oliver Thejl Eriksen, All rights reserved
# Licence:     GNU GPLv3
# -----------------------------------------------------------------------------
import random
import wave
import time
import copy
from pygame import mixer
mixer.init()

# Global constants. Read-only or deepcopied for use.
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
shipArray = [0, 1, 2, 1, 1]
gridX = 9
gridY = 9


# Parameter object that stores all needed information about a ships placement.
class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dirX = 0
        self.dirY = 0
        self.size = 0


# The class that controls a board. Two of these are instantiated.
class Board:
    def __init__(self, isPlayer):
        # Create two identical empty two-dimensional array.
        # These will be refered to as "the grid".
        self.visible = [[0 for rows in range(gridY)] for cols in range(gridX)]
        self.hidden = [[0 for rows in range(gridY)] for cols in range(gridX)]
        # Copy array of ships, make a counter of ships and a parameter object.
        self.shipArray = copy.deepcopy(shipArray)
        self.shipNum = sum(self.shipArray)
        self.shipParams = Ship()
        # Store number of total ships as a constant, for gameover condition.
        self.shipNumMax = self.shipNum
        # The smallest ship in shipArray. Is calculated when needed.
        self.minSize = 1

        # Variable for AI, saves coordinate of last hit ship.
        self.lastHit = []
        # Boolean for determining if board belongs to player or computer
        self.isPlayer = isPlayer

    # These two functions draw the grid. Only used for developing/debugging.
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

    # Checks if a ship could be placed with given parameters
    # Returns True if a ship can be placed, False if it cant.
    def is_ship_position_valid(self, ship: Ship, isMute: bool):
        # Calculate where the far end of ship is.
        lastX = (ship.size - 1) * ship.dirX + ship.x
        lastY = (ship.size - 1) * ship.dirY + ship.y
        # Checks if the far end of ship goes out of the grid.
        if(0 > lastX or lastX > gridX - 1):
            if(not isMute):
                PlayAudio("sfx_error")
                PlayAudio("i_out_of_bounds")
            return False

        # Exact same procedure for y-coordinate and rows.
        if(0 > lastY or lastY > gridY - 1):
            if(not isMute):
                PlayAudio("sfx_error")
                PlayAudio("i_out_of_bounds")
            return False

        # Iterates through all the squares that the ship goes through.
        for i in range(ship.size):
            x = i * ship.dirX + ship.x
            y = i * ship.dirY + ship.y
            # If there is anything BUT water on any square, its not valid.
            if(self.hidden[x][y] != 0):
                if(not isMute):
                    PlayAudio("sfx_error")
                    PlayAudio("i_occupied")
                return False

        return True

    # Adds a ship to the grid based on a given Ship object.
    # Only call this function after is_ship_position_valid() to avoid errors.
    def add_ship(self, ship: Ship):
        # Iterate through all the squares that the ship goes through.
        for i in range(ship.size):
            x = i * ship.dirX + ship.x
            y = i * ship.dirY + ship.y
            # Change information in the array to reflect the ship ID.
            # Ship ID is equal to shipNum at this moment in time.
            self.hidden[x][y] = self.shipNum
        # Reduce shipNum and thus the ship ID for the next ship.
        self.shipNum -= 1
        # Remove the used ship from shipArray.
        self.shipArray[ship.size - 1] -= 1

    # Checks if all squares of given shipID has been hit.
    def check_destroyed(self, shipID: int):
        # Checks if there exists a ship with the given shipID anywhere in grid.
        # If not, its because the ship has been destroyed.
        if(not any(shipID in sublist for sublist in self.hidden)):
            # Give sound feedback depending on whose ship got destroyed.
            if(self.isPlayer):
                PlayAudio("sfx_destroyed")
                PlayAudio("i_allied_ship_destroyed")
                self.clear_ai_memory(shipID)

            else:
                PlayAudio("sfx_destroyed")
                PlayAudio("i_enemy_ship_destroyed")

    def clear_ai_memory(self, shipID: int):
        self.lastHit.clear()
        for r in range(gridY):
            for c in range(gridX):
                # Change grid to reflect the ship is destroyed.
                if(self.hidden[c][r] == shipID + 10):
                    self.visible[c][r] = 3
                # Add back in remaining spotted ships that arent destroyed.
                if(self.visible[c][r] == 2):
                    self.lastHit.append(c)
                    self.lastHit.append(r)

    # Checks if all ships have been removed from the grid, meaning game over.
    # Returns True if game is over, False if game is still going on.
    def is_game_over(self):
        # For each ship ID,
        for i in range(1, self.shipNumMax + 1):
            # Iterate through the grid and return False if shipID is found.
            if(any(i in sublist for sublist in self.hidden)):
                return False
        # If nothing was found, return True (there are no ships left on grid).
        return True

    # Handles the placement of ships, has no return values or parameters.
    def ship_setup(self):
        for ships in range(self.shipNum):
            # If its a player, inform them what ships they have left.
            if (self.isPlayer):
                for i in range(len(self.shipArray)):
                    if (self.shipArray[i] == 0):
                        continue
                    PlayAudio("i_size_ava")
                    PlayAudio(str(i + 1))

            # Calculate minSize by iterating through shipArray.
            for i in range(len(self.shipArray)):
                if(self.shipArray[i] != 0):
                    self.minSize = i + 1
                    break

            # Reset ship parameter object.
            self.shipParams.size = self.minSize
            self.shipParams.x = 0
            self.shipParams.y = 0
            self.shipParams.dirX = 0
            self.shipParams.dirY = 0

            # Functions that determines and sets values for ship placement.
            self.set_coords()      # Sets x and y
            self.set_direction()   # Sets dirX and dirY
            self.set_size()        # Sets size

            # Place the ship at given values.
            self.add_ship(self.shipParams)

            # Audio feedback for player.
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
        # While loop is used as GOTO-statement with continue keyword.
        while(self.isPlayer):
            # Ask for coordinates, allow user to input before message is over.
            PlayAudio("q_coordinates", False)
            strCoords = input("Coordinates?")

            # Check if the inputted coordinates are valid.
            if(are_coords_valid(strCoords, True) is False):
                continue

            # Convert the string input into x and y integers.
            x, y = ConvertCoords(strCoords)

            # Check if square is empty on grid.
            if(self.hidden[x][y] != 0):
                # Position is not valid, a ship already occupies the spot.
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

            # Reset if no direction is valid for this coordinate and minSize.
            if(
                self.is_ship_position_valid(ship1, True) is False and
                self.is_ship_position_valid(ship2, True) is False and
                self.is_ship_position_valid(ship3, True) is False and
                self.is_ship_position_valid(ship4, True) is False
            ):
                # Audio feedback only given if all directions are blocked.
                PlayAudio("sfx_error")
                PlayAudio("i_no_space")
                continue

            # Inform player what coordinates they chose.
            PlayAudio("sfx_accept")
            PlayAudio("i_selected")
            PlayAudio(alphabet[x])
            PlayAudio(numbers[y])

            break

        # A non-player board does almost the same, but with no audio feedback.
        while(not self.isPlayer):
            strX = random.choice(alphabet)
            strY = random.choice(numbers)
            coordinates = strX + strY

            if(are_coords_valid(coordinates, True) is False):
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
                self.is_ship_position_valid(ship1, True) is False and
                self.is_ship_position_valid(ship2, True) is False and
                self.is_ship_position_valid(ship3, True) is False and
                self.is_ship_position_valid(ship4, True) is False
            ):
                continue

            break

    def set_direction(self):
        while(self.isPlayer):
            self.shipParams.dirX = 0
            self.shipParams.dirY = 0
            PlayAudio("q_direction", False)
            strDirection = input("Direction?").lower()

            # Parse input.
            if(strDirection in ["up", "u"]):
                self.shipParams.dirY = -1
                strDirection = "up"
            elif(strDirection in ["down", "d"]):
                self.shipParams.dirY = 1
                strDirection = "down"
            elif(strDirection in ["left", "l"]):
                self.shipParams.dirX = -1
                strDirection = "left"
            elif(strDirection in ["right", "r"]):
                self.shipParams.dirX = 1
                strDirection = "right"
            else:
                # If input could not be parsed, it must be invalid.
                PlayAudio("sfx_error")
                PlayAudio("i_invalid")
                continue

            # Reset if minimum size of ship doesnt fit.
            if(self.is_ship_position_valid(self.shipParams, False) is False):
                # Sound feedback comes from is_ship_position_valid().
                continue

            PlayAudio("sfx_accept")
            PlayAudio("i_selected")
            PlayAudio("i_" + strDirection)

            break

        while(not self.isPlayer):
            self.shipParams.dirX = 0
            self.shipParams.dirY = 0
            strDirection = random.choice(["up", "down", "left", "right"])

            if(strDirection in ["up"]):
                self.shipParams.dirY = -1
            elif(strDirection in ["down"]):
                self.shipParams.dirY = 1
            elif(strDirection in ["left"]):
                self.shipParams.dirX = -1
            elif(strDirection in ["right"]):
                self.shipParams.dirX = 1
            if(self.is_ship_position_valid(self.shipParams, True) is False):
                continue

            break

    def set_size(self):
        while(self.isPlayer):
            PlayAudio("q_size", False)
            strSize = input("Size of ship")

            # Is input an integer? Then parse it.
            try:
                size = int(strSize)
            except ValueError:
                # If not, restart while loop
                PlayAudio("sfx_error")
                PlayAudio("i_invalid")
                continue
            self.shipParams.size = int(strSize)

            # Does a ship of specified size exist?
            try:
                self.shipArray[self.shipParams.size - 1]
            except IndexError:
                PlayAudio("sfx_error")
                PlayAudio("i_no_exist_ship")
                continue

            # Does player have any ships of this size left?
            if(self.shipArray[self.shipParams.size - 1] == 0):
                PlayAudio("sfx_error")
                PlayAudio("i_no_ships_size")
                PlayAudio(strSize)
                continue

            # Can a ship be placed with that size?
            if(self.is_ship_position_valid(self.shipParams, False) is False):
                PlayAudio("i_choose_smaller")
                continue

            PlayAudio("sfx_accept")
            PlayAudio("i_selected")
            PlayAudio(strSize)

            break

        while(not self.isPlayer):
            strSize = str(random.randint(1, len(self.shipArray)))
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
            if(self.is_ship_position_valid(self.shipParams, True) is False):
                continue

            break


# Main function that calls all other functions.
def GameLoop():
    # TODO: Make automatic
    PlayAudio("q_tutorial", False)
    tutPlay = input("Do u want to hear a tutorial on how to play?")
    if (tutPlay == "y"):
        PlayAudio("i_tutorial")

    # Functions that only need to be called once.
    playerBoard = Board(True)
    computerBoard = Board(False)
    playerBoard.ship_setup()
    computerBoard.ship_setup()

    # The loop in which the game is played, only breaks on game over.
    while(True):
        # Players turn, they fire at the opponents board.
        FireAt(computerBoard, True)

        # Computers turn.
        FireAt(playerBoard, False)

        # Check if game is over and determine winner if neccesary.
        if(computerBoard.is_game_over() is True):
            if(playerBoard.is_game_over() is True):
                PlayAudio("i_tie")
            else:
                PlayAudio("i_win")
            break
        elif(playerBoard.is_game_over() is True):
            PlayAudio("i_loss")
            break


def FireAt(selectedB, isPlayer):
    x = 0
    y = 0
    limiter = 0
    while(isPlayer):
        PlayAudio("q_fire")
        coordinates = input("Where do you want to fire?")

        if(are_coords_valid(coordinates, True) is False):
            # Sound feedback comes from are_coords_valid().
            continue

        x, y = ConvertCoords(coordinates)

        if(selectedB.visible[x][y] > 0):
            PlayAudio("sfx_error")
            PlayAudio("i_already_fired")
            PlayAudio(alphabet[x])
            PlayAudio(numbers[y])
            continue

        PlayAudio("sfx_accept")
        PlayAudio("i_selected")
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])
        PlayAudio("sfx_fire")

        # Hit water.
        if(selectedB.hidden[x][y] == 0):
            selectedB.visible[x][y] = 1
            PlayAudio("sfx_miss")
            PlayAudio("i_miss")
        # Hit ship.
        else:
            # Update both grids
            selectedB.visible[x][y] = 2
            shipID = selectedB.hidden[x][y]
            selectedB.hidden[x][y] += 10
            PlayAudio("sfx_hit")
            PlayAudio("i_hit")
            selectedB.check_destroyed(shipID)

        break

    while(not isPlayer):
        # If computer hit something last turn, initiate AI algorhytm.
        # Programmers note: This algorhytm could be refactored to take up less
        # lines and have fewer comments, but this way its easier to read.
        if(selectedB.lastHit != []):
            # Create shorthand variable.
            r = selectedB.lastHit
            # If we hit multiple times, we can determine direction.
            if(len(r) > 2):
                # If x is same for both hits, ship must be differing on y.
                if(r[0] == r[2]):
                    # x should be the same value.
                    x = r[0]
                    # v is a sorted list of all y-coordinates in lasthits.
                    # k calculates distance between far ends of the ship.
                    v = sorted(r[1::2])
                    k = max(v) - min(v) + 2
                    # y then becomes either one below or one above lasthits.
                    y = v[0] - 1 + k * random.randint(0, 1)
                    # The two possible outcomes
                    temp1 = v[0] - 1 + k
                    temp2 = v[0] - 1
                    # If both outcomes are invalid (i.e. what the algorhytm
                    # thought was one ship in a line, is in reality multiple
                    # ships laying across)
                    cond1 = True
                    cond2 = True
                    if(temp1 < 0 or temp1 > gridY - 1):
                        cond1 = False
                    elif(selectedB.visible[x][temp1] > 0):
                        cond1 = False
                    if(temp2 < 0 or temp2 > gridY - 1):
                        cond2 = False
                    elif(selectedB.visible[x][temp2] > 0):
                        cond2 = False
                    if (cond1 is False and cond2 is False):
                        # Then select one of the y-values of lastHits and pick
                        # a new x which is nearby on x-axis
                        y = r[1]
                        b = sorted(r[::2])
                        h = max(b) - min(b) + 2
                        x = b[0] - 1 + h * random.randint(0, 1)
                # Same method, but reverse.
                elif(r[1] == r[3]):
                    y = r[1]
                    v = sorted(r[::2])
                    k = max(v) - min(v) + 2
                    x = v[0] - 1 + k * random.randint(0, 1)
                    temp1 = v[0] - 1 + k
                    temp2 = v[0] - 1
                    cond1 = True
                    cond2 = True
                    if(temp1 < 0 or temp1 > gridX - 1):
                        cond1 = False
                    elif(selectedB.visible[temp1][y] > 0):
                        cond1 = False
                    if(temp2 < 0 or temp2 > gridX - 1):
                        cond2 = False
                    elif(selectedB.visible[temp2][y] > 0):
                        cond2 = False
                    if (cond1 is False and cond2 is False):
                        x = r[0]
                        b = sorted(r[1::2])
                        h = max(b) - min(b) + 2
                        x = b[0] - 1 + h * random.randint(0, 1)
            # If we hit once, ship must be in one of the 4 adjacent squares
            else:
                # Same coordinates as lasthit, but add or remove one at random.
                temp = random.randint(0, 3)
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
        # If nothing was hit last turn, select completely randomly.
        else:
            x = random.choice(alphabet)
            y = random.choice(numbers)
            coordinates = x + y
            x, y = ConvertCoords(coordinates)

        if(x < 0 or y < 0):
            continue
        if(x > gridX - 1 or y > gridY - 1):
            continue
        if(selectedB.visible[x][y] > 0):
            continue

        PlayAudio("i_enemy_fire")
        PlayAudio(alphabet[x])
        PlayAudio(numbers[y])
        PlayAudio("sfx_fire")

        # Checks what was hit.
        if(selectedB.hidden[x][y] == 0):
            selectedB.visible[x][y] = 1
            PlayAudio("sfx_miss")
            PlayAudio("i_enemy_miss")
        else:
            selectedB.visible[x][y] = 2
            shipID = selectedB.hidden[x][y]
            selectedB.hidden[x][y] += 10
            PlayAudio("sfx_hit")
            PlayAudio("i_enemy_hit")

            # Add hit coordinates to AI memory.
            selectedB.lastHit.append(x)
            selectedB.lastHit.append(y)
            selectedB.check_destroyed(shipID)

        break


def are_coords_valid(coordinates: str, isMute: bool):
    # Not valid if input doesnt have exactly 2 characters.
    if len(coordinates) != 2:
        if(not isMute):
            PlayAudio("sfx_error")
            PlayAudio("i_invalid")
        return False

    # Parse input into seperate strings.
    temp = list(coordinates)
    x = temp[0].lower()
    y = temp[1].lower()

    # Check that input has exactly one number and one letter.
    if(x not in alphabet and x not in numbers):
        if(not isMute):
            PlayAudio("sfx_error")
            PlayAudio("i_invalid")
        return False
    if(y not in alphabet and y not in numbers):
        if(not isMute):
            PlayAudio("sfx_error")
            PlayAudio("i_invalid")
        return False
    if(x in alphabet and y in alphabet):
        if(not isMute):
            PlayAudio("sfx_error")
            PlayAudio("i_invalid")
        return False
    if(x in numbers and y in numbers):
        if(not isMute):
            PlayAudio("sfx_error")
            PlayAudio("i_invalid")
        return False

    return True


# Returns the integers x and y, that corresponds to given coordinates.
def ConvertCoords(coordinates: str):
    temp = list(coordinates)
    x = temp[0].lower()
    y = temp[1].lower()

    # Make sure x is first.
    try:
        int(y)
    except ValueError:
        x, y = y, x

    # Make both integers for easier use in program.
    x = alphabet.index(x)
    y = numbers.index(y)

    return x, y


# Plays one .wav soundfile with given filename.
def PlayAudio(fileName, sleep=True):
    path = "audio/" + fileName + ".wav"
    mixer.music.load(path)
    mixer.music.play()
    if(sleep):
        # Calculate how long the audioclip is.
        wr = wave.open(path, "r")
        frames = wr.getnframes()
        frameRate = wr.getframerate()
        duration = frames / frameRate
        # Sleep system for that long.
        time.sleep(duration)


# Start the game by calling GameLoop() once.
GameLoop()

# Prevent game from closing instantly after GameLoop() is over.
input("Press enter to exit")
