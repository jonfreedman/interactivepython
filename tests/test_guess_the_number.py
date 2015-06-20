from com.github.jonfreedman.interactivepython import guess_the_number as guess

def test_new_game_starts_at_zero_to_ninetynine():
    game = guess.Game()
    assert game.game_range == 100
    assert game.max_guesses == 7
    assert game.guess_count == 0

def test_can_always_guess_with_a_new_game():
    game = guess.Game()
    assert game.can_guess()

def test_guessing_increments_guess_count():
    game = guess.Game()
    game.guess(50)
    assert game.guess_count == 1

def test_resetting_game_keeps_current_range():
    game = guess.Game()
    game.guess(50)
    game.reset()
    assert game.guess_count == 0
