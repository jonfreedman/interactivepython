import random

__author__ = 'jon'


def name_to_number(name):
    """convert name to number."""
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    raise ValueError("Cannot play with " + name)


def number_to_name(number):
    """convert number to a name."""
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    raise ValueError(number + " is not valid")


def rpsls(player_choice):
    """Play rock, paper, scissors, lizard, Spock."""
    # print a blank line to separate consecutive games
    print("")

    # print out the message for the player's choice
    print("Player chooses " + player_choice)

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)

    # print out the message for computer's choice
    print("Computer chooses " + comp_choice)

    # compute difference of comp_number and player_number modulo five
    result = (comp_number - player_number) % 5

    # use if/elif/else to determine winner, print winner message
    if result == 0:
        print("Player and computer tie!")
    elif result < 3:
        print("Computer wins!")
    else:
        print("Player wins!")


def main():
    """play the game"""
    rpsls("rock")
    rpsls("Spock")
    rpsls("paper")
    rpsls("lizard")
    rpsls("scissors")

if __name__ == '__main__':
    main()
