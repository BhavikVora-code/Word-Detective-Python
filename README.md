# Mini-Project: Word Detective

**Project Type:** Python Command-Line Game (Guess the word by letter)
**Team Members:** Bhavik Vora and Vishal Tulaskar

### 1. What is Word Detective?
Word Detective is a Python terminal game that puts a spin on classic word-guessing games like Hangman. Instead of guessing completely blind, the player is given a trivia clue at the start of the round. The goal is to figure out the hidden word before making 6 wrong guesses. We also added a scoring system where players earn points based on the length of the word and how many lives they had left.

### 2. How We Split the Work (Team of 2)
Since there were two of us, we split the project into coding and game design/testing:
* **Bhavik Vora (Coder):** I was responsible for writing the actual Python code. I built the while loops, the scoring math, the menu system, and figured out how to make the code do what we wanted it to do.
* **Vishal Tulaskar (Game Design & Testing):** My partner acted as the guide for the project. He came up with the dictionary of words, sorted them into categories, and wrote all the clues. He also playtested the game constantly to find bugs or things that felt annoying to play, which told me what I needed to fix in the code.

### 3. Difficulties We Faced and How We Fixed Them
While making this game, we ran into a few annoying problems that we had to figure out how to solve:

**Difficulty 1: The game was too repetitive to play**
At first, every time you finished guessing a word, the game kicked you all the way back to the main menu. You had to type "1" and press Enter every single time you wanted to play another round, which totally ruined the fun.
* **Our Fix:** We added a 5-second timer to the game loop. Now, if you win a round, the game pauses for 5 seconds so you can see your score, and then it automatically starts the next word. We also made it so that if you lose, it breaks the streak and sends you back to the main menu.

**Difficulty 2: Typing out words you already knew**
Sometimes the trivia clue made the answer obvious right away. But in our early version, you were forced to guess it one letter at a time, which felt tedious.
* **Our Fix:** I changed the code that asks for the player's guess. I added a rule that checks the length of what the user typed. If they type a full word and it matches the secret word, they get an "Instant Solve" and win the round immediately.

**Difficulty 3: Unexpected crash errors**
When my partner was testing the game, he tried to close it by pressing Ctrl+C on his keyboard (which is a common way to force-close terminal programs). Instead of closing nicely, the game would crash and show a long, confusing error message on the screen.
* **Our Fix:** I learned about "exception handling." At the very bottom of the code, I put our main menu inside a try/except block. Now, if the game detects that the player pressed Ctrl+C, it prevents the error message from showing and simply prints "Game closed. Goodbye, Detective." before shutting down gracefully.
