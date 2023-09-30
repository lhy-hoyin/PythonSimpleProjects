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
    if len(s) < 1: raise "Nothing to encode"

    output = ""
    words = s.split(' ')

    for w in words:

        is_capitalized = w[0].isupper()
        has_symbol = not w.isalpha()

        w_ = w

        # TODO: handle symbols

        # TODO: handle 1-char words

        # First character is a vowel
        if is_vowel(w[0]):
            output += (w_.capitalize() if is_capitalized else w_) + "way "
            continue

        # First character is a consonant, only need check second character

        w_ = w.lower()
        w_out = ""

        if is_vowel(w_[1]):
            # first letter of the word at the end of the word
            w_out = w_[1:] + w_[0]
        else:
            # move the two consonants to the end of the word
            w_out = w_[2:] + w_[:2]

        w_out = (w_out.capitalize() if is_capitalized else w_out)
        print(w_out)

        output += w_out + "ay "
    
    return output.strip()

def decode(s: str) -> str :
    if len(s) < 1: raise "Nothing to decode"
    # TODO

if __name__ == "__main__":
    #print(encode("Hello world!"), "\n")
    print(encode("Witch"), "\n")

    assert encode("Happy") == "Appyhay"
    assert encode("Awesome") == "Awesomeway"
    assert encode("Childe") == "Ildechay"
    # assert encode("Pig Latin is hard to speak.") == "Igpay Atinlay isway ardhay otay eakspay."
    assert encode("Witch") == "Itchway" # TODO: how to decode this
