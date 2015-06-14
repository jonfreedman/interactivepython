from com.github.jonfreedman.interactivepython.rpsls import name_to_number, number_to_name

def test_name_to_number():
    assert name_to_number("rock") == 0
    assert name_to_number("Spock") == 1
    assert name_to_number("paper") == 2
    assert name_to_number("lizard") == 3
    assert name_to_number("scissors") == 4

def test_number_to_name():
    assert number_to_name(0) == "rock"
    assert number_to_name(1) == "Spock"
    assert number_to_name(2) == "paper"
    assert number_to_name(3) == "lizard"
    assert number_to_name(4) == "scissors"