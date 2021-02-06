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
    print("Enter any single digit to quit.")

    #TODO - find a random word, must block single char words, maybe added a min-char limit for generates word
    mysteryWord = "HelloWorld"
    #mysteryWord = mysteryWord.upper() # Convert to caps

    # Convert mysteryWord to list of dict
    word = []
    for char in mysteryWord.upper():
        word.append({char : False}) # False flag to hide letter

    # Continue game if player still have lives
    while (livesCount > 0 and not solvedFlag):
        correctGuess = False
        print() #creates newline

        # Display lives left
        print("Life: ", end = '')
        for x in range(livesCount):
            print(LIVES_UNICODE, end=" ") 
        print() # creates newline
        
        # Display current word status
        print("Mystery Word: ", end = '')
        for char in word:
            print(list(char.keys())[0] if list(char.values())[0] else '*', end = '')
        print() # creates newline

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
                print("You have entered a digit. Quitting...")
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
