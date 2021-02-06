'''
Author: BarryHY
Project Name: Hangman
Description: Guess the word within the given attempts/lives
'''

def main():
    
    # CONSTANTS - may be customised accordingly
    LIVES = 6
    LIVES_UNICODE = u'\u2665' #heart icon
    
    print("===================")
    print("= = = HANGMAN = = =")
    print("===================")

    livesCount = LIVES
    solvedFlag = False

    print("You have %d attempts to guess the word." % LIVES)
    print("Enter any digit to quit.")

    #TODO - find a random word
    mysteryWord = "helloworld"
    mysteryWord = mysteryWord.upper() # Convert to caps

    # Convert mysteryWord to list of dict
    word = []
    for char in mysteryWord:
        word.append({char : False}) # False flag to hide letter

    # Continue game if player still have lives
    while (livesCount > 0 and not solvedFlag):
        solvedFlag = True # set flag for condition checking later
        correctGuess = False
        print() #creates newline

        # Display lives left
        print("Live(s): ", end = '')
        for x in range(livesCount):
            print(LIVES_UNICODE, end=" ") 
        print() # creates newline
        
        # Display current word status
        print("Mystery Word: ", end = '')
        for char in word:
            print(list(char.keys())[0] if list(char.values())[0] else '*', end = '')
        print() # creates newline

        # Takes 1st char input, only, convert to caps
        letter = input("Choose a single letter: ")[0].upper()
        
        # Check for exiting condition
        if letter.isnumeric():
            print("You have entered a digit. Quitting...")
            break; # exit game loop
        
        # Check if player guess is correct
        for char_dict in word:
            char = list(char_dict.keys())[0]
            charSolved = list(char_dict.values())[0]
            
            # Matching character
            if (letter == char):
                correctGuess = True
                charSolved = True
                char_dict[char] = charSolved # Show letter

            # Update unsolvedFlag
            solvedFlag = solvedFlag and charSolved

        # Provide feedback on player's guess
        if correctGuess:
            print("%s is a correct letter." % letter)
        else: # Deduct life for incorrect guess
            livesCount = livesCount - 1
            print("Sorry, wrong guess. You lost a life.")

    print() # create newline

    # Player has solved the mystery word
    if solvedFlag:
        print("Congratulations! You solved \'%s\' with %d %s left." % (mysteryWord, livesCount, ("lives" if livesCount > 1 else "life")))

    # Player has lost all lives
    if livesCount < 1:
        print("Game Over! You have no lives left.")

    # Finish game
    print("Thank you for playing!")



if __name__ == "__main__":
    main()
