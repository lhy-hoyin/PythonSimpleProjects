'''
Author: BarryHY
Date Created: 29 Jan 2021
Date Updated: 12 Feb 2021
Project Name: Hangman
Description: Guess the word within the given attempts/lives. Multiple modes available.

Library Required: RandomWords (https://pypi.org/project/RandomWords/)
'''

import enchant
from getpass import getpass
from random_words import RandomWords

# Game Parameters - may be customised accordingly
LIVES = 6
BONUS_LIVES = 4
ENABLE_HINTS = True
LIVES_UNICODE = u'\u2665' #heart icon

def main():
    print("===================")
    print("= = = HANGMAN = = =")
    print("===================")

    # Create dictionary for language spelling checks
    dicts = []
    dicts.append(enchant.Dict("en_US"))
    dicts.append(enchant.Dict("en_GB"))
    
    # Game Loop
    while (True):
        # Display main menu to select playing mode
        print("\n[Main Menu]")
        print("[1] Play against computer")
        print("[2] Play against another player")
        print("[Q] Quit Game")
        
        choice = input(">>>")[0] # only take first char
        
        # Play against computer
        if choice == '1':
            # Randomly generate a word
            randomWord = RandomWords().random_word()
            
            # Start game with the random word (with bonus lives)
            guess_the_word(randomWord, lives = LIVES + BONUS_LIVES)
            
        # Play against another player
        if choice == '2':
            # Prompt player 1 to provide input
            print("\nPlayer One,")
            while True:
                givenWord = getpass("Please enter a WORD for Player Two to guess: (just type, word is hidden)")
                if check_word(dicts, givenWord):
                    break # only if word is considered as valid
            givenHint = input("Please enter a HINT to help Player Two: ")
            
            # Start game with player 1's word
            print("\nPlayer Two,")
            guess_the_word(givenWord, hint = givenHint)
        
        # Quit game
        if choice.upper() == 'Q':
            print("Thank you for playing!")
            break

def guess_the_word(mysteryWord:str, hint:str = None, lives:int = LIVES):
    solvedFlag = False
    
    print("\nYou have %d lives to guess the word." % lives)
    print("Enter any single digit to go back to main menu.")

    # Convert mysteryWord to list of dict
    word = []
    for char in mysteryWord.upper():
        word.append({char : False}) # False flag to hide letter

    # Continue game if player still have lives
    while (lives > 0 and not solvedFlag):
        correctGuess = False # reset flag
        print() # creates newline

        # Display lives left
        print("Life: ", end = '')
        for x in range(lives):
            print(LIVES_UNICODE, end=" ") 
        print() # creates newline
        
        # Display current word status
        print("Mystery Word: ", end = '')
        for char in word:
            print(list(char.keys())[0] if list(char.values())[0] else '*', end = '')
        print() # creates newline

        if(ENABLE_HINTS and hint != None):
            print("Hint: " + hint)

        # Takes in user input
        userInput = input("Choose a SINGLE letter or type out your WHOLE guess: ")
        
        # Player choose to guess the whole word
        if len(userInput) > 1:
            # Player guessed correctly
            if mysteryWord.upper() == userInput.upper():
                correctGuess = True
                solvedFlag = True

        # Player choose to guess a single letter
        else:
            # Takes 1st char only, convert to caps
            letter = userInput[0].upper()
        
            # Check for exiting condition
            if letter.isnumeric():
                print("You have entered a digit. Back to main menu...")
                break; # exit game loop
            
            solvedFlag = True # set flag for condition checking later

            # Check if player guess is correct
            for char_dict in word:
                char = list(char_dict.keys())[0]
                charSolved = list(char_dict.values())[0]
            
                # Matching character
                if (letter == char):
                    correctGuess = True
                    charSolved = True
                    char_dict[char] = charSolved # Show letter

                # Update solvedFlag
                solvedFlag = solvedFlag and charSolved

            if correctGuess:
                print("%s is a correct letter." % letter)
        
        # Deduct live for incorrect guess
        if not correctGuess:
            lives -= 1
            print("Sorry, wrong guess. You lost a life.") 

    # Player has solved the mystery word
    if solvedFlag:
        print("Congratulations! You solved \'%s\' with %d %s left." % (mysteryWord, lives, ("lives" if lives > 1 else "life")))

    # Player has lost all lives, reveal mysteryWord
    if lives < 1:
        print("Game Over! You have no lives left. The mystery word is \'%s\'." % mysteryWord)

'''
Checks if given word is considered valid

parameter   [List]dictionaries  Language dictionaries to check spelling against
parameter   [String]word        The word to check for validity and spelling
return      [Boolean]           True if the word is valid
'''
def check_word(dictionaries: list, word:str) -> bool:  
    # Check that is fully alphabet
    if not word.isalpha():
        print("Please only type ONE word - no space, dots, dashes, numbers, etc.")
        return False
        
    # Check spelling to ensure word is spelled correctly
    for langDict in dictionaries:
        # If one if the language dictionary says the word is spelled correctly, then word is considered valid
        if langDict.check(word):
            return True
    # None of the dictionary considers word as spelled correctly
    print("Sorry, word not recognised. Please check spelling or choose another word.")
    return False

if __name__ == "__main__":
    main()
