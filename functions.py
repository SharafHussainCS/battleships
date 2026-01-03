from colorama import Fore, Style
import random
from copy import deepcopy

# Function used to print out battle grid for every turn in the game
def battleGrid(ships, grid, hits):
    if grid == 4:
        print("   𝒜 𝐵 𝒞 𝒟")
    elif grid == 6:
        print("   𝒜 𝐵 𝒞 𝒟 𝐸 𝐹")
    for i in range(grid*grid):
        if ((grid == 4 and i%4 == 0) or (grid == 6 and i%6 == 0)):
            if (i != 0):
                print()
            print(f"{int(i//grid)+1} ", end="")
        if (i in hits) and (i in ships):
            print("🟥", end="")
        elif (i in hits):
            print("🟩", end="")
        elif (i in ships):
            print("🟦", end="")
        else:
            print("⬜", end="")
        if i == ((grid*grid)-1):
            print("\n")

# Function that converts coordinate value to a integer value on the grid
def coordinate(cord, grid):
    if grid == 4:
        numbers = [1, 2, 3, 4]
        letters = ["a", "b", "c", "d"]
    elif grid == 6:
        numbers = [1, 2, 3, 4, 5, 6]
        letters = ["a", "b", "c", "d", "e", "f"]
    cord = cord.lower()
    if (len(cord) != 2) or (cord[0] not in letters) or (int(cord[1]) not in numbers):
        return -100
    cordLetter = letters.index(cord[0])
    cordNum = int(cord[1])
    convert = (cordLetter + (grid*(cordNum-1))) 
    return convert

# Function that converts integer value to coordinate valye on the grid
def cords(cord, grid):
    numbers = [1, 2, 3, 4, 5, 6]
    letters = ["a", "b", "c", "d", "e", "f"]
    letter = letters[cord%grid]
    number = numbers[cord//grid]
    number = str(number)
    convert = (letter + number).upper()
    return convert

# Random ship generator and player ship generation for each game and gamemode
def shipGenerator(numShips, grid, player):
    gridSize = list(range(grid*grid))
    ships = []
    temp = -100
    for i in range(numShips):
        gridSizeTemp = deepcopy(gridSize)
        while True:
            shipLocation = -100 # Dummy value
            if (player):
                battleGrid(ships, grid, [])
                print("Cordinate by Cordinate enter ships")
                while (shipLocation == -100):
                    cord = str(input("Enter Coordinate: "))
                    shipLocation = coordinate(cord, grid)
            else:
                shipLocation = random.choice(gridSizeTemp)
            shipRow  = shipLocation//grid
            extendChoices = [grid, -grid, 1, -1]
            if shipLocation not in ships:
                if ((shipLocation + grid) not in gridSize) and ((shipLocation - grid) not in gridSize) and ((shipLocation + 1) not in gridSize) and ((shipLocation - 1) not in gridSize):
                    gridSizeTemp.remove(shipLocation)
                    continue
                if (((shipLocation + grid)//grid) != shipRow) and (((shipLocation - grid)//grid) != shipRow) and (((shipLocation + 1)//grid) != shipRow) and (((shipLocation - 1)//grid) != shipRow):
                    gridSizeTemp.remove(shipLocation)
                    continue
                while True:
                    shipExtention = 100 # Dummy Value
                    if (player):
                        while (shipExtention not in extendChoices) or (temp == -100):
                            cord = str(input("Enter Adjacent Coordinate: "))
                            temp = coordinate(cord, grid)
                            shipExtention = temp - shipLocation
                    else:
                        shipExtention  = random.choice(extendChoices)
                    shipLocation2 = shipLocation + shipExtention
                    if (shipLocation2 not in gridSize):
                        extendChoices.remove(shipExtention)
                        continue 
                    if ((shipExtention == 1) or (shipExtention  ==  -1)) and (shipLocation2//grid != shipRow):
                        extendChoices.remove(shipExtention)
                        continue
                    gridSize.remove(shipLocation)
                    gridSize.remove(shipLocation2)
                    ships.append(shipLocation)
                    ships.append(shipLocation2)
                    break
                break
            else:
                try:
                    gridSize.remove(shipLocation)
                finally:
                    continue
    return ships

# Helper function for the shipGenerator, as it take the list gained from shipGenerator and sorts it in a 2D array
# This is meant for to seperate the 2 locations of the ships into their own list
def shipSorter(allShips):
    shipsSorted = []
    for i in range(0, len(allShips), 2):
        shipsSorted.append([allShips[i], allShips[i+1]])
    return shipsSorted

# This function insure that user input is always correct between 2-3 options
def correctInput(x, y, z):
    if (z == ""): # This makes the function usable for 2 or 3 options inputs
        z = y
        keyboard = input(f"{x} or {y}: ")
    else:
        keyboard = input(f"{x}, {y} or {z}: ")
    while True:
        if (keyboard[:2].lower() == x[:2].lower()):
            return x
        elif (keyboard[:2].lower() == y[:2].lower()):
            return y
        elif (keyboard[:2].lower() == z[:2].lower()):
            return z
        if (z == y):
            keyboard = input(f"Please enter either {x} or {y}: ")
        else:
            keyboard = input(f"Please enter either {x}, {y} or {z}: ")

# Function prints out the leaderboard screen
def leaderboard():
    top5 = [["", -1],["", -1],["", -1],["", -1],["", -1]]
    with open("battleships.txt", "r") as file:
        for line in file:
            line = (line.rstrip()).split(",")
            score = int(line[2])
            for i in range(5):
                if (score > top5[i][1]):
                    top5.insert(i, [line[0], score])
                    top5.pop()
                    break
    print(f"{Fore.RED}{Style.BRIGHT}LEADERBOARD{Fore.YELLOW}{Style.BRIGHT}")
    for i in range(5):
        print(f"{top5[i][0]}: {top5[i][1]}")
    print(f"{Fore.BLUE}{Style.BRIGHT}")
    option = correctInput("Menu", "Login Page", "")
    return option

# Function clears the console from text
def clearConsole():
    print("\033[H\033[J")     