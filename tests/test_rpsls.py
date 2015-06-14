from com.github.jonfreedman.interactivepython import rpsls

def test_name_to_number():
    assert rpsls.name_to_number("rock") == 0
    assert rpsls.name_to_number("Spock") == 1
    assert rpsls.name_to_number("paper") == 2
    assert rpsls.name_to_number("lizard") == 3
    assert rpsls.name_to_number("scissors") == 4

def test_number_to_name():
    assert rpsls.number_to_name(0) == "rock"
    assert rpsls.number_to_name(1) == "Spock"
    assert rpsls.number_to_name(2) == "paper"
    assert rpsls.number_to_name(3) == "lizard"
    assert rpsls.number_to_name(4) == "scissors"