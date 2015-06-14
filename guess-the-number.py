"""
Play guess the number using SimpleGUICS2Pygame

All output for the game will be printed in the console

.. _SimpleGUICS2Pygame:
   https://simpleguics2pygame.readthedocs.org
"""

__author__ = 'jon'

import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

game_range = 100
max_guesses = 7
guess_count = 0

secret_number = 0

def new_game():
    """helper function to start and restart the game"""
    global guess_count, secret_number
    guess_count = 0
    secret_number = random.randrange(0, game_range)
    print("Started a new game, guess in [0," + str(game_range) + ")")

# define event handlers for control panel
def range100():
    global game_range, max_guesses
    game_range = 100
    max_guesses = 7
    new_game()

def range1000():
    global game_range, max_guesses
    game_range = 1000
    max_guesses = 10
    new_game()

def input_guess(guess):
    """Compare guess against secret number"""
    try:
        numeric_guess = int(guess)
    except ValueError:
        raise ValueError(guess + " is not a valid guess")

    print("Guess was " + str(numeric_guess))

    if numeric_guess == secret_number:
        print("Correct")
        new_game()
        return

    global guess_count
    guess_count += 1
    if guess_count == max_guesses:
        print("Value was " + str(secret_number) + r"""
_____.___.              .____
\__  |   | ____  __ __  |    |    ____  ______ ____
 /   |   |/  _ \|  |  \ |    |   /  _ \/  ___// __ \
 \____   (  <_> )  |  / |    |__(  <_> )___ \\  ___/
 / ______|\____/|____/  |_______ \____/____  >\___  >
 \/                             \/         \/     \/
""")
        new_game()
    elif numeric_guess < secret_number:
        print("Lower")
    else:
        print("Higher")

    print(str(max_guesses - guess_count) + " guesses remaining...")

# create frame
frame = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements and start frame
frame.add_input("Guess:", input_guess, 100)
frame.add_button("Range: 0 - 100", range100, 100)
frame.add_button("Range: 0 - 1000", range1000, 100)

new_game()
frame.start()