import random

#word database
WORDS = []


# validates the language
def validate_feedback(feedback):
    """
    DFA that accepts strings of length 5
    over alphabet { '/', '-', 'x' }
    """

    state = 0

    for ch in feedback:
        if ch not in ['/', '-', 'x']:
            return False  #invalid symbol

        state += 1

        if state > 5:
            return False  #too long

    return state == 5  #must end exactly at q5


#eliminates words
def filter_words(word_list, guess, feedback):
    new_words = []

    for word in word_list:
        valid = True

        #Track used letters (for correct matching)
        word_chars = list(word)
        used = [False] * 5

        #STEP 1: Handle "/" (correct position)
        for i in range(5):
            if feedback[i] == '/':
                if word[i] != guess[i]:
                    valid = False
                    break
                used[i] = True

        if not valid: #remove words if it doesnt have a correct letter, correct position
            continue

        #STEP 2: Handle "-" (misplaced letters)
        for i in range(5):
            if feedback[i] == '-':
                found = False

                for j in range(5):
                    if not used[j] and word[j] == guess[i] and j != i:
                        found = True
                        used[j] = True
                        break

                if not found: #if a misplaced letter is not found in the word, remove it
                    valid = False
                    break

        if not valid:
            continue

        # STEP 3: Handle "x" (not in word)
        for i in range(5):
            if feedback[i] == 'x':
                #if a word already deemed not there contains a letter not in your word, remove it
                if guess[i] in [word[j] for j in range(5) if not used[j]]:
                    valid = False
                    break

        if valid:
            new_words.append(word)

    return new_words


#Main game
def play_game():
    print("\nThink of a 5-letter word.\n")
    print("I will try to guess it in 6 attempts.")
    print("After each guess, provide feedback in a string of exactly 5 characters\n")
    print("our Language consist of {w | w ∈ { '/', '-', 'x' }*5}\n")
    print("Analyze my guess, wherein '/' means correct letter and position, '-' means correct letter but wrong position, and 'x' means the letter is not in the word.")
    print('Type "yes" when ready.')

    ready = input("> ").strip().lower()

    if ready != "yes":
        print("Restarting...")
        return

    print("\nFeedback format:")
    print('"/" = correct, "-" = wrong position, "x" = not in word')
    print("Example: /-x--")

    possible_words = WORDS.copy()
    attempts = 6

    while attempts > 0:
        if not possible_words:
            print("\nYour chosen word does not exist in my database.")
            return

        guess = random.choice(possible_words) #choose random valid word based on what it knows
        print(f"\nSystem guess: {guess}")

        #loop until valid input WITHOUT changing guess
        while True:
            feedback = input("Enter feedback: ").strip()

            if not validate_feedback(feedback):
                print("Invalid input. Use exactly 5 symbols: / - x")
                continue

            break  # valid input → exit loop

        if feedback == "/////":
            print("Guessed Correctly, so your word is: " + guess)
            return

        possible_words = filter_words(possible_words, guess, feedback)
        attempts -= 1
        print(f"Attempts left: {attempts}")

    print("\nFailed to guess within 6 attempts.")
    #print out possible remaining words
    if possible_words:
        print("Possible remaining words were: " + ", ".join(possible_words))
    else:
        print("No possible words remain based on feedback.")


def main():
    
    #get a list of valid words from file
    with open("valid-wordle-words.txt", "r") as f:
        for line in f:
            word = line.strip().lower()
            if len(word) == 5 and word.isalpha():
                WORDS.append(word)
    
    while True:
        play_game()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again != "yes":
            print("Goodbye!")
            break



if __name__ == "__main__":
    main()