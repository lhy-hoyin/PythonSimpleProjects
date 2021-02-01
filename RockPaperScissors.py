'''
Author: BarryHY
Date Created: 29 Jan 2021
Date Updated: 01 Feb 2021
Project Name: Rock, Paper, Scissors Game
Description: User to play rock, paper, scissors with the computer
'''

import random

def main():
    
    # CONSTANTS - may be changed accordingly
    QUIT_COMMAND = "Quit"
    
    print("=================================")
    print("= = = ROCK, PAPER, SCISSORS = = =")
    print("=================================")
    
    random.seed()
    winScore, loseScore, drawScore = 0,0,0
    dict_ = {
        0 : QUIT_COMMAND,
        1 : "Rock",
        2 : "Paper",
        3 : "Scissors",
    }
    
    '''
    print("Enter 0 to quit.\n")
    '''
    # or you can use this code so that it's not hard-coded
    for key in dict_:
        if (dict_[key] == QUIT_COMMAND):
            print("Enter %d to quit." % key)
    #'''
    
    while True:
        # Display possible moves
        print() # create a blank line
        for key in dict_:
            print(str(key) + ": " + dict_[key])
        player = int(input("Choose your move: "))
        
        # Check for valid input
        if (player not in dict_):
            print("Invalid input. Try again.")
            continue
        
        # Check for quitting condition
        if (dict_[player] == QUIT_COMMAND):
            print("Thank you for playing!")
            break
            
        # Generated opponent move
        opponent = random.randint(1, 3) #fixme: hard-coded(!)

        print(dict_[player] + " VS " + dict_[opponent])
        
        # Same move - Draw
        if (player == opponent):
            print("Result: Draw")
            drawScore+=1
            continue
            
        # Different Move - Win/Lose
        if (player%3 < opponent%3):
            loseScore+=1
            print("Result: Lose :(")
        else:
            winScore+=1
            print("Result: Win :)")
    
    # Print stats summary
    print("Win: %d | Lose: %d | Draw: %d" % (winScore, loseScore, drawScore))
            
if __name__ == "__main__":
    main()
