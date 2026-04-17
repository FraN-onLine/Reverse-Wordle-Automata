import random

# -----------------------------
# WORD DATABASE (you can expand this)
# -----------------------------
WORDS = [
    "apple", "grape", "crate", "slate", "trace",
    "stone", "plane", "flame", "brake", "crane",
    "glare", "share", "spare", "score", "shore"
]

# -----------------------------
# DFA VALIDATOR FOR FEEDBACK
# -----------------------------
def validate_feedback(feedback):
    """
    DFA that accepts strings of length 5
    over alphabet { '/', '-', 'x' }
    """

    # State simulation: q0 → q1 → q2 → q3 → q4 → q5
    state = 0

    for ch in feedback:
        if ch not in ['/', '-', 'x']:
            return False  # invalid symbol → dead state

        state += 1

        if state > 5:
            return False  # too long

    return state == 5  # must end exactly at q5


# -----------------------------
# FILTER WORDS BASED ON FEEDBACK
# -----------------------------
def filter_words(word_list, guess, feedback):
    new_words = []

    for word in word_list:
        valid = True

        # Track used letters (for correct matching)
        word_chars = list(word)
        used = [False] * 5

        # STEP 1: Handle "/" (correct position)
        for i in range(5):
            if feedback[i] == '/':
                if word[i] != guess[i]:
                    valid = False
                    break
                used[i] = True

        if not valid:
            continue

        # STEP 2: Handle "-" (misplaced letters)
        for i in range(5):
            if feedback[i] == '-':
                found = False

                for j in range(5):
                    if not used[j] and word[j] == guess[i] and j != i:
                        found = True
                        used[j] = True
                        break

                if not found:
                    valid = False
                    break

        if not valid:
            continue

        # STEP 3: Handle "x" (not in word)
        for i in range(5):
            if feedback[i] == 'x':
                # check if guess[i] appears anywhere UNUSED
                if guess[i] in [word[j] for j in range(5) if not used[j]]:
                    valid = False
                    break

        if valid:
            new_words.append(word)

    return new_words


# -----------------------------
# MAIN GAME FUNCTION
# -----------------------------
def play_game():
    print("\nThink of any 5-letter word from my database.")
    ready = input('Type "yes" when ready: ').strip().lower()

    if ready != "yes":
        print("Okay, restarting...")
        return

    possible_words = WORDS.copy()
    attempts = 6

    while attempts > 0:
        if not possible_words:
            print("\nYour chosen word does not exist in my database.")
            return

        guess = random.choice(possible_words)
        print(f"\nSystem guess: {guess}")

        feedback = input("Enter feedback (/ for correct, - for misplaced, x for not in word): ").strip()

        if not validate_feedback(feedback):
            print("❌ Invalid input. Must be exactly 5 characters using only '/', '-', 'x'.")
            continue

        if feedback == "/////":
            print("🎉 Guessed correctly!")
            return

        possible_words = filter_words(possible_words, guess, feedback)
        attempts -= 1
        print(f"Attempts left: {attempts}")

    print("\n❌ Failed to guess within 6 attempts.")


# -----------------------------
# REPLAY LOOP
# -----------------------------
def main():
    while True:
        play_game()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again != "yes":
            print("Goodbye!")
            break


# -----------------------------
# RUN PROGRAM
# -----------------------------
if __name__ == "__main__":
    main()