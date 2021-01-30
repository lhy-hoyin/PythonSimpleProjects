'''
Author: BarryHY
Project Name: Guess The Number
Description: Program randomly generate a number. Player to guess what the number is.
             If wrong, tell player guess is either too high, or too low.
'''

import random

def main():
    
    # CONSTANTS - can be changed accordingly (eg. increase/decrease difficulty)
    MIN_NUMBER = 0
    MAX_NUMBER = 20
    
    print("============================")
    print("= = = GUESS THE NUMBER = = =")
    print("============================")
    
    triesCount = 0
    random.seed()
    number = random.randint(MIN_NUMBER, MAX_NUMBER)
    
    while True:
        guess = int(input("\nGuess a number between " + str(MIN_NUMBER) + " and " + str(MAX_NUMBER) + ": "))
        triesCount+=1
        if (guess == number):
            print("Congratulations! You took " + str(triesCount) + (" tries " if triesCount > 1 else " try ")+ "to guess the number correctly.")
            break
        elif (guess > number):
            print("Your guess is too high. Try again.")
        elif (guess < number):
            print("Your guess is too low. Try again.")
        


if __name__ == "__main__":
    main()