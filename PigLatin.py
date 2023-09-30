"""
Author: lhy-hoyin
Date Created: 30 Sep 2023
Date Updated: 30 Sep 2023
Project Name: Pig Latin
Description: Encode or decode pig latin

Reference:
    https://web.ics.purdue.edu/~morelanj/RAO/prepare2.html
"""

import re

def is_consonant(s: str) -> bool :
    return not is_vowel(s)
    
def is_vowel(s: str) -> bool :
    if len(s) != 1: 
        raise "Can only check one character"
    return s in "AaEeIiOoUu"

def encode(s: str) -> str :
    if len(s) < 1:
        raise "Nothing to encode"

    output = ""
    tokens = re.split('([^a-zA-Z])', s)

    for t in tokens:

        # Not a word, probably a symbol
        if not t.isalpha():
            output += t
            continue

        is_capitalized = t[0].isupper()
        word = t.lower()
        
        # First character is a vowel
        if is_vowel(word[0]):
            output += (word.capitalize() if is_capitalized else word) + "way"
            continue

        '''
        Note: English only have 'I' and 'A/a' as one-letter words
              which has been handled by the first-letter-vowel case above.

              Check is still done below, in case the `s` has been cipher-encoded
              in some other way, which results in non-vowel one-letter words.
        '''

        if len(word) == 1:
            output += (word.capitalize() if is_capitalized else word) + "ay"
            continue

        # First character is a consonant, only need check second character
        

        if is_vowel(word[1]):
            # move first letter of the word at the end of the word
            word = word[1:] + word[0]
        else:
            # move the two consonants to the end of the word
            word = word[2:] + word[:2]

        output += (word.capitalize() if is_capitalized else word) + "ay"

    return output.strip()

def decode(s: str) -> str :
    if len(s) < 1: raise "Nothing to decode"
    # TODO

if __name__ == "__main__":
    assert encode("Happy") == "Appyhay" # C + V
    assert encode("Awesome") == "Awesomeway" # V
    assert encode("Childe") == "Ildechay" # C + C

    assert encode("I am a car") == "Iway amway away arcay" # One-letter words

    # With symbols
    assert encode("127.0.0.1") == "127.0.0.1"
    assert encode("Hello, World!") == "Ellohay, Orldway!"
    assert encode("Pig Latin is hard to speak.") == "Igpay Atinlay isway ardhay otay eakspay."

    # TODO: how to decode this
    SAME_STRING = "Itchway"
    assert encode("Witch") == SAME_STRING
    assert encode("Itch") == SAME_STRING
    
