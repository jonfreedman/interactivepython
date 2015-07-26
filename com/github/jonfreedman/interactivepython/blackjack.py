"""Mini-Project: Week 2."""

from __future__ import print_function
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


class Card(object):
    """Single playing card."""

    def __init__(self, suit, rank):
        """New card."""
        if not ((suit in SUITS) and (rank in RANKS)):
            raise ValueError("Invalid card: ", suit, rank)
        self.suit = suit
        self.rank = rank
        self.turned = False

    def __str__(self):
        """Print suit and rank."""
        return self.suit + self.rank

    def get_suit(self):
        """Card suit."""
        return self.suit

    def get_rank(self):
        """Card rank."""
        return self.rank

    def turn(self):
        """Turn the card."""
        self.turned = not self.turned

    def draw(self, canvas, pos):
        """Draw the card."""
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if self.turned:
            canvas.draw_image(CARD_IMAGES, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                              CARD_SIZE)
        else:
            canvas.draw_image(CARD_BACK, CARD_BACK_CENTER, CARD_SIZE,
                              [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_BACK_SIZE)


class Hand(object):
    """Blackjack hand of cards."""

    def __init__(self):
        """Create empty hand."""
        self.cards = []

    def __str__(self):
        """Print all cards."""
        return ", ".join([str(card) for card in self.cards])

    def add_card(self, card):
        """Add a card."""
        self.cards.append(card)

    def get_value(self):
        """Count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust."""
        base = sum([VALUES.get(card.get_rank()) for card in self.cards])
        if "A" in [card.get_rank() for card in self.cards] and base <= 11:
            return base + 10
        return base

    def draw(self, canvas, pos):
        """Draw a hand of cards."""
        for index, card in enumerate(self.cards):
            card.draw(canvas, (pos[0] + (index * 100), pos[1]))


class Deck(object):
    """Deck of 52 cards."""

    def __init__(self):
        """Create un-shuffled deck."""
        self.cards = [Card(s, r) for s in SUITS for r in RANKS]

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal_card(self, turn):
        """Deal a card object from the deck."""
        card = self.cards.pop(0)
        if turn:
            card.turn()
        return card

    def __str__(self):
        """Print all cards."""
        return ", ".join([str(card) for card in self.cards])


class Blackjack(object):
    """Game of Blackjack with one player and a dealer."""

    def __init__(self):
        """Start a new game."""
        self.deck = Deck()
        self.dealer = Hand()
        self.player1 = Hand()
        self.in_play = False
        self.score = 0
        self.message = ""

    def deal(self):
        """Deal a fresh hand."""
        self.deck.cards.extend(self.dealer.cards)
        self.deck.cards.extend(self.player1.cards)
        self.deck.shuffle()
        for card in self.deck.cards:
            if card.turned:
                card.turn()
        self.dealer = Hand()
        self.player1 = Hand()
        self.player1.add_card(self.deck.deal_card(True))
        self.dealer.add_card(self.deck.deal_card(False))
        self.player1.add_card(self.deck.deal_card(True))
        self.dealer.add_card(self.deck.deal_card(True))
        self.message = "Player 1 to play..."
        if self.in_play:
            self.message = "Folded, player 1 to play..."
            self.score -= 1
        self.in_play = True
        if self.player1.get_value() == 21:
            self.stand()

    def hit(self):
        """Player requests a card."""
        if self.in_play:
            self.player1.add_card(self.deck.deal_card(True))
            if self.player1.get_value() >= 21:
                self.stand()

    def stand(self):
        """Player stands, dealer plays."""
        if self.in_play:
            self.dealer.cards[0].turn()
            while self.dealer.get_value() < 17:
                self.dealer.add_card(self.deck.deal_card(True))
            if self.player1.get_value() > 21:
                self.message = "You are bust, new deal?"
                self.score -= 1
            elif self.player1.get_value() > self.dealer.get_value():
                self.message = "Player 1 wins, new deal?"
                self.score += 1
            elif self.dealer.get_value() > 21:
                self.message = "Dealer bust, new deal?"
                self.score += 1
            else:
                self.message = "Dealer wins, new deal?"
                self.score -= 1
            self.in_play = False

    def draw(self, canvas):
        """Draw the game."""
        canvas.draw_text("Blackjack", (50, 80), 48, "#2EFEC8", "sans-serif")
        canvas.draw_text("Score " + str(self.score), (380, 80), 24, "black", "sans-serif")
        canvas.draw_text("Dealer", (50, 180), 24, "black", "sans-serif")
        canvas.draw_text("Player 1", (50, 380), 24, "black", "sans-serif")
        canvas.draw_text(self.message, (200, 380), 24, "black", "sans-serif")
        self.dealer.draw(canvas, (50, 240))
        self.player1.draw(canvas, (50, 420))


CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_IMAGES = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
CARD_BACK = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

GAME = Blackjack()


def main():
    """
    Blackjack.

    .. _SimpleGUICS2Pygame:
       https://simpleguics2pygame.readthedocs.org
    """
    frame = simplegui.create_frame("Blackjack", 600, 600)
    frame.set_canvas_background("Green")

    frame.add_button("Deal", GAME.deal, 200)
    frame.add_button("Hit", GAME.hit, 200)
    frame.add_button("Stand", GAME.stand, 200)
    frame.set_draw_handler(GAME.draw)

    frame.start()


if __name__ == '__main__':
    main()
