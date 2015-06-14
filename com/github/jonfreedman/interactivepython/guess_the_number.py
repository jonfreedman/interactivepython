"""Mini-Project: Week 2."""

from __future__ import print_function
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'


class Game(object):

    """Holds the game state."""

    def __init__(self):
        """Instantiate a new game picking a random number in [0, 100)."""
        self.set_config(100, 7)

    def set_config(self, game_range, max_guesses):
        """Set the game configuration and start a new game.

        :param game_range: upper bound for number
        :param max_guesses: maximum number of guesses allowed
        """
        self.game_range = game_range
        self.max_guesses = max_guesses
        self.reset()

    def reset(self):
        """Reset the game state, set guess_count to 0 and pick a new number."""
        self.guess_count = 0
        self.secret_number = random.randrange(0, self.game_range)
        print("Started a new game, guess in [0," + str(self.game_range) + ")")

    def guess(self, guess):
        """Record a guess.

        :param guess: the guess
        """
        self.guess_count += 1
        return guess == self.secret_number

    def can_guess(self):
        """Check if further guesses are possible

        :returns: True if another guess is possible
        """
        return self.guess_count < self.max_guesses


GAME = Game()


# define event handlers for control panel
def range100():
    """Start a new game using [0,100)."""
    GAME.set_config(100, 7)


def range1000():
    """Start a new game using [0,1000)."""
    GAME.set_config(1000, 10)


def input_guess(guess):
    """Guess event handler, compare guess against secret number."""
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

    frame.start()

if __name__ == '__main__':
    main()
