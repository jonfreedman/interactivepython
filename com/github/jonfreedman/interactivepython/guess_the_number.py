"""Mini-Project: Week 2"""

from __future__ import print_function
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'


class Game:
    """Holds the game state."""
    def __init__(self, game_range, max_guesses):
        self.game_range = game_range
        self.max_guesses = max_guesses
        self.reset()

    def reset(self):
        self.guess_count = 0
        self.secret_number = random.randrange(0, self.game_range)
        print("Started a new game, guess in [0," + str(self.game_range) + ")")

    def guess(self, x):
        self.guess_count += 1
        return x == self.secret_number

    def can_guess(self):
        return self.guess_count < self.max_guesses


GAME = Game(100, 7)


def _new_game(game_range, max_guesses):
    """helper function to start and restart the game."""
    global GAME
    GAME = Game(game_range, max_guesses)


# define event handlers for control panel
def range100():
    """Start a new game using [0,100)."""
    _new_game(100, 7)


def range1000():
    """Start a new game using [0,1000)."""
    _new_game(1000, 10)


def input_guess(guess):
    global GAME

    """Compare guess against secret number."""
    try:
        numeric_guess = int(guess)
    except ValueError:
        print(guess + " is not a valid guess")
        return

    print("Guess was " + str(numeric_guess))

    if GAME.guess(numeric_guess):
        print("Correct")
        GAME.reset()
        return

    if not GAME.can_guess():
        print("Value was " + str(GAME.secret_number) + r"""
_____.___.              .____
\__  |   | ____  __ __  |    |    ____  ______ ____
 /   |   |/  _ \|  |  \ |    |   /  _ \/  ___// __ \
 \____   (  <_> )  |  / |    |__(  <_> )___ \\  ___/
 / ______|\____/|____/  |_______ \____/____  >\___  >
 \/                             \/         \/     \/
""")
        GAME.reset()
    elif numeric_guess < GAME.secret_number:
        print("Lower")
    else:
        print("Higher")

    print(str(GAME.max_guesses - GAME.guess_count) + " guesses remaining...")


def main():
    """
    Play guess the number, all output for the game will be printed in the console.

    .. _SimpleGUICS2Pygame:
       https://simpleguics2pygame.readthedocs.org
    """
    # create frame
    frame = simplegui.create_frame("Guess the number", 300, 300)

    # register event handlers for control elements and start frame
    frame.add_input("Guess:", input_guess, 100)
    frame.add_button("Range: 0 - 100", range100, 100)
    frame.add_button("Range: 0 - 1000", range1000, 100)

    range100()
    frame.start()

if __name__ == '__main__':
    main()
