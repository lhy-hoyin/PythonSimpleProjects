import random


difficulty_options = {
    # level difficulty: length of secret
    1: 4,
    2: 6,
    3: 8
}


emoji_result = "✅❔❌"

def result(idx: int) -> str:
    return emoji_result[idx:idx+1]


emoji_numbers = "0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣"

def numbers(x: str) -> str:
    if len(x) == 1:
        i = int(x) * 3
        return emoji_numbers[i:i+3] + "  "
    else:
        return numbers(x[0]) + numbers(x[1:])
    

def generate_random_number(length: int) -> str:
    lower_limit = 10 ** (length - 1)
    upper_limit = 10 ** length - 1
    random_number = random.randint(lower_limit, upper_limit)
    return str(random_number)


def give_hints(guess: str, secret: str) -> str:
    assert(len(guess) == len(secret))

    hint = ""

    for g, s in zip(guess, secret):
        if (g == s):
            hint += result(0)
        elif g in secret:
            hint += result(1)
        else:
            hint += result(2)

        hint += " "

    return hint
    

if __name__ == "__main__":

    # Prompt user to select difficulty
    while True:
        choice = input(f"Please choose a difficulty {list(difficulty_options)}: ")
        
        # Input validation
        if not choice.isdigit():
            print("Input not a number.")
            continue
        elif int(choice) not in difficulty_options.keys():
            print(f"Input not a valid difficulty. Choose: {list(difficulty_options)}")
            continue
        else:
            difficulty = int(choice)
            break

    print(f"""======================================
    \rRules:
    \r- Left-most digit will never be a {numbers("0")}.
    \r- Digits can be repeated.
    \r""")

    secret_length = difficulty_options.get(difficulty)
    secret = generate_random_number(secret_length)
    # print(f"Shhhh! The secret is {numbers(secret)}.")

    turn_count = 1
    guess_log = []
    while True:

        while True:
            guess = input(f"The secret is {secret_length}-digits long. Guess: ")

            if len(guess) == secret_length:
                break
            else:
                print("Your guess is the wrong length.")

        if guess == secret:
            break # Correct guess
        else:
            # Wrong guess, give hints.
            guess_log.append(f"{numbers(guess)}")
            guess_log.append(give_hints(guess, secret))

            # Print guess history
            for text in guess_log:
                print(text)

        turn_count += 1

    # Correct code
    print(f"Correct! You took {turn_count} guess(es) to crack the code "
          f"{numbers(secret)}.")
