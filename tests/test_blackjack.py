from com.github.jonfreedman.interactivepython import blackjack

def test_card_has_suit_and_rank():
    card = blackjack.Card("S", "A")
    assert card.get_suit() == "S"
    assert card.get_rank() == "A"

def test_hand_can_have_cards_added_and_keeps_score():
    hand = blackjack.Hand()
    hand.add_card(blackjack.Card("S", "A"))
    assert hand.get_value() == 11
    hand.add_card(blackjack.Card("C", "2"))
    assert hand.get_value() == 13
    hand.add_card(blackjack.Card("D", "T"))
    assert hand.get_value() == 13
    hand.add_card(blackjack.Card("D", "A"))
    assert hand.get_value() == 14
    hand.add_card(blackjack.Card("C", "A"))
    assert hand.get_value() == 15

def test_deck_has_cards():
    deck = blackjack.Deck()
    card = deck.deal_card()
    assert card is not None

def test_deck_can_be_shuffled():
    deck = blackjack.Deck()
    card = deck.deal_card()
    assert card is not None

def test_hands_are_dealt():
    game = blackjack.Blackjack()
    game.deal()
    assert len(game.player1.cards) == 2
    assert len(game.dealer.cards) == 2
    while game.player1.get_value() < 17:
        game.hit()
    game.stand()
    assert game.player1.get_value() >= 17
    assert game.dealer.get_value() >= 17

def test_dealing_in_game_loses():
    game = blackjack.Blackjack()
    game.deal()
    assert game.score == 0
    game.deal()
    assert game.score == -1