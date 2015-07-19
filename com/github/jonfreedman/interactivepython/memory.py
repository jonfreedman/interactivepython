"""Mini-Project: Week 1."""

from __future__ import print_function
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'


class Card(object):
    """Single card in the game."""

    def __init__(self, value):
        self.value = value
        self.visible = False

    def turn(self):
        self.visible = not self.visible

    def draw(self, canvas, x_offset):
        if self.visible:
            canvas.draw_polygon([(x_offset + 2, 2), (x_offset + 2, CANVAS_HEIGHT - 2), (x_offset + CARD_WIDTH - 2, CANVAS_HEIGHT - 2), (x_offset + CARD_WIDTH - 2, 2)], 2, 'Green')
            canvas.draw_text(str(self.value), [x_offset + 10, CANVAS_HEIGHT - 30], 64, 'White')
        else:
            canvas.draw_polygon([(x_offset + 2, 2), (x_offset + 2, CANVAS_HEIGHT - 2), (x_offset + CARD_WIDTH - 2, CANVAS_HEIGHT - 2), (x_offset + CARD_WIDTH - 2, 2)], 2, 'Green', 'Green')

class Game(object):
    """Memory game state."""

    def __init__(self, label=None):
        self.deck = [Card(i) for i in list(range(8)) * 2]
        random.shuffle(self.deck)
        self.turns = 0
        self.state = 0
        self.card1 = None
        self.card2 = None
        self.label = label
        if label is not None:
            self.label.set_text("Turns = 0")

    def user_click(self, index):
        if self.deck[index].visible:
            # clicked an already visible card, do nothing
            pass
        else:
            if self.state == 0:
                # click with no card turned
                self.state = 1
                self.card1 = self.deck[index]
                self.card1.turn()
            elif self.state == 1:
                # click with one card turned
                self.state = 2
                self.card2 = self.deck[index]
                self.card2.turn()
            else:
                # click with two cards turned
                self.state = 1
                if self.card1.value != self.card2.value:
                    # not matched
                    self.card1.turn()
                    self.card2.turn()
                self.take_turn()
                self.card1 = self.deck[index]
                self.card2 = None
                self.card1.turn()


    def take_turn(self):
        self.turns += 1
        self.label.set_text("Turns = " + str(self.turns))


CANVAS_HEIGHT = 100
CANVAS_WIDTH = 800
GAME = Game()
CARD_WIDTH = (CANVAS_WIDTH / len(GAME.deck))


def new_game(label):
    """Start a new game."""
    GAME.__init__(label)


def mouseclick(pos):
    """Handle clicks on cards."""
    GAME.user_click(int(pos[0] // CARD_WIDTH))


def draw(canvas):
    """Draw cards in a row."""
    for index, card in enumerate(GAME.deck):
        card.draw(canvas, index * CARD_WIDTH)


def main():
    """
    Memory.

    .. _SimpleGUICS2Pygame:
       https://simpleguics2pygame.readthedocs.org
    """
    frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
    label = frame.add_label("Turns = 0")
    frame.add_button("Reset", lambda: new_game(label))
    frame.set_mouseclick_handler(mouseclick)
    frame.set_draw_handler(draw)

    new_game(label)
    frame.start()


if __name__ == '__main__':
    main()
