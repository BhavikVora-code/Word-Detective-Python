import random
import textwrap
import time
from words_list import WORDS

MAX_WRONG_GUESSES = 6
AUTO_HINT_EVERY = 3


HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """
]

def display_hangman(wrong_guesses):
    print(HANGMAN_STAGES[min(wrong_guesses, MAX_WRONG_GUESSES)])

def show_hint_box(hint):
    width = 44
    lines = textwrap.wrap(hint, width)
    border = "+" + "-" * (width + 2) + "+"
    print("\n" + border)
    print("| " + "CASE CLUE".ljust(width) + " |")
    print("| " + " " * width + " |")
    for line in lines:
        print("| " + line.ljust(width) + " |")
    print(border)

def display_word(word, guessed_letters):
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in word
    )

def reveal_random_letter(word, guessed_letters):
    hidden_letters = [
        letter for letter in set(word)
        if letter not in guessed_letters
    ]
    if len(hidden_letters) <= 1:
        return None
    letter = random.choice(hidden_letters)
    guessed_letters.add(letter)
    return letter

def choose_word(used_words):
    all_choices = [
        (category, word, hint)
        for category, items in WORDS.items()
        for word, hint in items.items()
    ]
    
    available = [item for item in all_choices if item[1] not in used_words]
    
    if not available:
        used_words.clear()
        available = all_choices

    available_categories = list(set([item[0] for item in available]))
    chosen_category = random.choice(available_categories)
    
    words_in_category = [item for item in available if item[0] == chosen_category]
    category, word, hint = random.choice(words_in_category)
    
    used_words.add(word)
    return category, word, hint

def play_game(used_words, career_score):
    category, word, hint = choose_word(used_words)
    guessed_letters = set()
    wrong_guesses = 0
    print("\n=======================================")
    print("          CASE FILE OPENED")
    print("=======================================")
    print(f"Category: {category}")
    print(f"Word length: {len(word)} letters")
    print("Commands: type a letter, guess the full word, or QUIT")
    print(f"A free random letter is revealed every {AUTO_HINT_EVERY} wrong guesses.")
    show_hint_box(hint)
    
    while True:
        print("\n" + "=" * 39)
        display_hangman(wrong_guesses)
        print("Word: " + display_word(word, guessed_letters))
        print(f"Wrong guesses: {wrong_guesses}/{MAX_WRONG_GUESSES}")
        print(f"Lives remaining: {MAX_WRONG_GUESSES - wrong_guesses}")
        print(f"Career Score: {career_score}")
        guessed_display = ", ".join(sorted(guessed_letters))
        print("Guessed/revealed letters:", guessed_display or "None")
        
        if wrong_guesses >= MAX_WRONG_GUESSES:
            print("\nCASE FAILED! The stickman is complete.")
            print(f"The correct word was: {word.upper()}")
            print("Payout: 0 points")
            return career_score, False 
            
        if all(letter in guessed_letters for letter in set(word)):
            base_score = len(word) * 10
            lives_bonus = (MAX_WRONG_GUESSES - wrong_guesses) * 20
            round_score = base_score + lives_bonus
            career_score += round_score
            print("\nCASE SOLVED! You guessed the word!")
            print(f"The word was: {word.upper()}")
            print("\n--- ROUND PAYOUT ---")
            print(f"Base Score ({len(word)} letters) : +{base_score}")
            print(f"Lives Bonus ({MAX_WRONG_GUESSES - wrong_guesses} remaining) : +{lives_bonus}")
            print("-" * 20)
            print(f"TOTAL ROUND SCORE       :  {round_score}")
            print(f"NEW CAREER SCORE        :  {career_score}")
            return career_score, True 
            
        guess = input("\nEnter a letter/word, ? to read clue again, or QUIT: ").strip().lower()
        
        if guess == "quit":
            print("You left this case without solving it.")
            print(f"The correct word was: {word.upper()}")
            return career_score, False
            
        if guess in ("?", "hint"):
            show_hint_box(hint)
            continue
            
        if not guess.isalpha():
            print("Enter letters only, ? to read clue again, or QUIT.")
            continue
            
        if len(guess) > 1:
            if guess == word:
                print("\n*** INCREDIBLE DETECTIVE WORK! INSTANT SOLVE! ***")
                guessed_letters.update(set(word)) 
            else:
                wrong_guesses += 1
                print(f"Incorrect! '{guess.upper()}' is not the hidden word.")
            continue
            
        if guess in guessed_letters:
            print("You have already guessed or revealed that letter!")
            continue
            
        guessed_letters.add(guess)
        
        if guess in word:
            print(f"Correct! '{guess.upper()}' is in the word.")
        else:
            wrong_guesses += 1
            print(f"Incorrect! '{guess.upper()}' is not in the word.")
            if (wrong_guesses % AUTO_HINT_EVERY == 0 and wrong_guesses < MAX_WRONG_GUESSES):
                revealed = reveal_random_letter(word, guessed_letters)
                if revealed:
                    print("\n*** AUTOMATIC HINT UNLOCKED! ***")
                    print(f"The game revealed the letter {revealed.upper()}!")
                else:
                    print("Only one letter remains, no automatic hint is given.")

def show_instructions():
    print("\n========== HOW TO PLAY ==========")
    print("1. Read the case file clue provided at the start of the round.")
    print("2. Guess the hidden word one letter at a time, OR type the full word to instantly solve!")
    print("3. Every wrong guess adds a body part to the stickman.")
    print(f"4. {MAX_WRONG_GUESSES} wrong guesses means game over.")
    print(f"5. Every {AUTO_HINT_EVERY} wrong guesses, a random hidden letter is revealed.")
    print("\n--- HIGH STAKES SCORING ---")
    print("6. You ONLY earn points if you solve the case (0 points for failing).")
    print("7. Winning payout = (Word Length x 10) + (Remaining Lives x 20).")
    print("8. Type QUIT during a round to leave it.")
    print("=================================")

def main():
    used_words = set()
    career_score = 0
    while True:
        print("\n")
        print("=" * 39)
        print("            WORD DETECTIVE")
        print("=" * 39)
        print(f"Career Score: {career_score} pts")
        print("1. Play Game")
        print("2. Instructions")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            while True:
                career_score, keep_playing = play_game(used_words, career_score)
                
                if not keep_playing:
                    break 
                    
                print("\nStarting next case in 5 seconds...")
                time.sleep(5)
                
        elif choice == "2":
            show_instructions()
            
        elif choice == "3":
            print(f"\nFinal Career Score: {career_score} pts")
            print("Thanks for playing Word Detective!")
            print("Goodbye, Detective.")
            break
            
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nGame closed. Goodbye, Detective.")