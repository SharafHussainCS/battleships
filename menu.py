from time import sleep
from colorama import Fore, Style
import sys
from functions import clearConsole, correctInput, shipGenerator, shipSorter, leaderboard
from game import game

'''
Problem Description:
A competitive battle ship game is needed to be produced. A sign-in and
login-in page must be made where account data can be saved to be accessed on a later date.
A menu page must be included where you can "play" or access the "leaderboard"
to see the which player has the most score in the game.
The battle ship game itself must consist of two game modes a 4 by 4 game
consisting 2 ships each side, and a 6 by 6 game consisting 5 ships each side.
Score must be added or deducted from the account's user depending if they win or lose the game to the computer.
   '''

startingLogo = """                                                          
     ____    _  _____ _____ _     _____ ____  _   _ ___ ____  ____  
    | __ )  / \|_   _|_   _| |   | ____/ ___|| | | |_ _|  _ \/ ___| 
    |  _ \ / _ \ | |   | | | |   |  _| \___ \| |_| || || |_) \___ \ 
    | |_) / ___ \| |   | | | |___| |___ ___) |  _  || ||  __/ ___) |
    |____/_/   \_|_|   |_| |_____|_____|____/|_| |_|___|_|   |____/ 
                                                                    
"""


startingText = "Welcome to Competitive Battle Ships!"

# Account function after player logs-in
def setUp(username):
    clearConsole()
    print(f"Welcome Back {username}!\n")
    print("Battle Mode: (4 by 4)")
    print("War Mode: (6 by 6)\n")
    option = correctInput("Battle", "War", "Exit")
    if (option == "Battle"):
        grid = 4
        computerShips = shipGenerator(2, 4, False)
        playerShips = shipGenerator(2, 4, True)
    elif (option  == "War"):
        grid = 6
        computerShips = shipGenerator(5, 6, False)
        playerShips = shipGenerator(5, 6, True)
    else:
        menu()
    computerShipsSorted = shipSorter(computerShips)
    playerShipsSorted = shipSorter(playerShips)
    clearConsole()
    print("LET THE GAMES BEGIN")
    sleep(1)
    clearConsole()
    match = game(playerShips, playerShipsSorted, computerShips, computerShipsSorted, grid, username)
    setUp(match)

# Menu function / Starting Screen 
def menu():
    clearConsole()
    print(f"{Fore.BLUE}{Style.BRIGHT}{startingLogo}\n{startingText}")
    option = correctInput("Play Now", "Leaderboard", "Exit")
    if (option == "Play Now"):
        clearConsole()
        option = correctInput("Login", "Sign Up", "")
        if (option == "Sign Up"):
            signUp()
            print("CONGRATS ON THE NEW ACCOUNT")
            print("Taking you to the menu....")
            sleep(2)
            menu()
        else:
            setUp(login())
    elif (option == "Leaderboard"):
        clearConsole()
        option = leaderboard()
        if option == "Menu":
            menu()
        else:
            login()
    else:
        sys.exit()

# Login function for existing user
def login():
    clearConsole()
    usernameReal = False
    passwordReal = False
    while((not usernameReal) or (not passwordReal)):
        usernameReal = False
        passwordReal = False
        username = input(f"{Fore.GREEN}{Style.BRIGHT}Username:{Fore.BLUE}{Style.BRIGHT} ")
        password = input(f"{Fore.GREEN}{Style.BRIGHT}Password:{Fore.BLUE}{Style.BRIGHT} ")
        with open("battleships.txt", "r") as file:
            for line in file:
                line = (line.rstrip()).split(",")
                if (line[0].lower() == username.lower()):
                    usernameReal = True
                    if (line[1] == password):
                        passwordReal = True
                        return line[0]
            if (usernameReal == False):
                print("There is no such username in the database")
            elif (usernameReal == True and passwordReal == False):
                print("Password does not match username\n")
        option = correctInput("Try Again", "Menu", "Exit")
        clearConsole()
        if option == "Menu":
            menu()
        elif option == "Exit":
            sys.exit()
            
    print("ENTERED")

# Sign-Up function for new user
def signUp():
    with open("battleships.txt", "a") as file:
        username = signUpHelper("Username")
        password = signUpHelper("Password")
        file.write(f"{username},{password},0\n")

# Small helper function to check is password and username are acceptable
# Function is for both "username" and "password," as the signUp code would be doubled without this function
def signUpHelper(form):
    condition = True
    while condition:
        condition = False
        word = input(f"Create a {form}: ")
        if (len(word) == 0):
            print("Please enter atleast 1 character")
            condition = True
        for i in range(len(word)):
            if word[i] == ",":
                print("Sorry the inclustion of ',' in the username or password is not allowed")
                condition = True
        if (form == "Username"):
            with open("battlships.txt", "r") as file:
                for line in file:
                    line = (line.rstrip()).split(",")
                    if (line[0].lower() == word.lower()):
                        print("This username is already taken")
                        condition = True
    return word

            
if __name__ == "__main__":
    menu()