from time import sleep
from functions import clearConsole, cords, battleGrid, coordinate
import random
from copy import deepcopy

# Funtion for the actual battle ships game 
def game(p, pSorted , c, cSorted, grid, username):
    pFixed = deepcopy(p)
    playerShots = []
    playerHits = []
    computerHits = []
    computerChoices = list(range(grid*grid))
    while (len(p) != 0) and (len(c) != 0):
        sleep(2)
        clearConsole()
        print("\nCOMPUTERS TURN\n")
        computerBomb = random.choice(computerChoices)
        computerChoices.remove(computerBomb)
        computerHits.append(computerBomb)
        if computerBomb in p:
            print(f"HIT ON {cords(computerBomb, grid)}")
            p.remove(computerBomb)
            for i in range(len(pSorted)):
                if computerBomb in pSorted[i]:
                    pSorted[i].remove(computerBomb)
                    if len(pSorted[i]) == 0:
                        print("SHIP SUNK")
                    break
            if (len(p) == 0):
                battleGrid(pFixed, grid, computerHits)
                print("COMPUTER WINS")
                gameScore(username, False, grid)
                continue
        else:
            print(f"MISS ON {cords(computerBomb, grid)}")
        battleGrid(pFixed, grid, computerHits)
        print("\nYOUR TURN\n")
        battleGrid(playerShots, grid, playerHits)
        playerBomb = input("Drop a Bomb on: ")
        playerBomb = coordinate(playerBomb, grid)
        while (playerBomb == -100) or (playerBomb in playerHits):
            playerBomb = input("Please Enter a Proper Coordinate: ")
            playerBomb = coordinate(playerBomb, grid)
        playerHits.append(playerBomb)
        if playerBomb in c:
            playerShots.append(playerBomb)
            print(f"HIT ON {cords(playerBomb, grid)}")
            c.remove(playerBomb)
            for i in range(len(cSorted)):
                if playerBomb in cSorted[i]:
                    cSorted[i].remove(playerBomb)
                    if len(cSorted[i]) == 0:
                        print("SHIP SUNK")
                    break
        else:
            print(f"MISS ON {cords(playerBomb, grid)}")
        battleGrid(playerShots, grid, playerHits)
        if (len(c) == 0):
            print("PLAYER WINS")
            gameScore(username, True, grid)
    print("Ruturning to menu....")
    sleep(4)
    return username

# Functions manages score after each game, helping update the account satistics
def gameScore(username, winBoolean, grid):
    change = -10
    if winBoolean:
        if grid == 4:
            change = 10
        elif grid == 6:
            change = 15
    with open("battleships.txt", "r") as file:
        for account in file:
            account = (account.rstrip()).split(",")
            if (account[0] == username):
                password = account[1]
                score = account[2]
    with open("battleships.txt", "r") as file:
        lines = file.readlines()
    with open("battleships.txt", "w") as file:
        for line in lines:
            if line != f"{username},{password},{score}\n":
                file.write(line)
            else:
                score = int(score)
                score += change
                file.write(f"{username},{password},{score}\n")
 
