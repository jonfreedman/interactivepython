"""
Play guess the number using SimpleGUICS2Pygame

All output for the game will be printed in the console

.. _SimpleGUICS2Pygame:
   https://simpleguics2pygame.readthedocs.org
"""

import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'

GAME_RANGE = 100
MAX_GUESSES = 7
GUESS_COUNT = 0

SECRET_NUMBER = 0


def new_game():
    """helper function to start and restart the game"""
    global GUESS_COUNT, SECRET_NUMBER
    GUESS_COUNT = 0
    SECRET_NUMBER = random.randrange(0, GAME_RANGE)
    print("Started a new game, guess in [0," + str(GAME_RANGE) + ")")


# define event handlers for control panel
def range100():
    global GAME_RANGE, MAX_GUESSES
    GAME_RANGE = 100
    MAX_GUESSES = 7
    new_game()


def range1000():
    global GAME_RANGE, MAX_GUESSES
    GAME_RANGE = 1000
    MAX_GUESSES = 10
    new_game()


def input_guess(guess):
    """Compare guess against secret number"""
    try:
        numeric_guess = int(guess)
    except ValueError:
        raise ValueError(guess + " is not a valid guess")

    print("Guess was " + str(numeric_guess))

    if numeric_guess == SECRET_NUMBER:
        print("Correct")
        new_game()
        return

    global GUESS_COUNT
    GUESS_COUNT += 1
    if GUESS_COUNT == MAX_GUESSES:
        print("Value was " + str(SECRET_NUMBER) + r"""
_____.___.              .____
\__  |   | ____  __ __  |    |    ____  ______ ____
 /   |   |/  _ \|  |  \ |    |   /  _ \/  ___// __ \
 \____   (  <_> )  |  / |    |__(  <_> )___ \\  ___/
 / ______|\____/|____/  |_______ \____/____  >\___  >
 \/                             \/         \/     \/
""")
        new_game()
    elif numeric_guess < SECRET_NUMBER:
        print("Lower")
    else:
        print("Higher")

    print(str(MAX_GUESSES - GUESS_COUNT) + " guesses remaining...")


def main():
    # create frame
    frame = simplegui.create_frame("Guess the number", 300, 300)

    # register event handlers for control elements and start frame
    frame.add_input("Guess:", input_guess, 100)
    frame.add_button("Range: 0 - 100", range100, 100)
    frame.add_button("Range: 0 - 1000", range1000, 100)

    new_game()
    frame.start()


if __name__ == '__main__':
    main()