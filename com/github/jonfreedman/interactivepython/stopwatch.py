"""
Stopwatch: The Game.

Stop the timer to the second exactly to score a point

Timer colours courtesy of http://tinyurl.com/mopmdyn

.. _SimpleGUICS2Pygame:
   https://simpleguics2pygame.readthedocs.org
"""

import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'

# define global variables
TIME = 0
COLOUR = "#FFFFFF"
RUNNING = False
POINTS = 0
STOPS = 0

FONT = "monospace"
SCORE_SIZE = 24
TIME_SIZE = 36

def format(t):
    """Convert time in tenths of a second into a formatted string A:BC.D."""
    mins = "%d" % (t // 600)
    secs = "%02d" % ((t // 10) % 60)
    tenths = "%d" % (t % 10)
    return mins + ":" + secs + "." + tenths

def colour_picker():
    """Generate a random 2-digit hex pastel colour."""
    return (255 + random.randrange(0, 256)) / 2

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    """Start the timer."""
    global timer, RUNNING
    timer.start()
    RUNNING = True

def stop():
    """Stop the timer and check if a point is scored."""
    global timer, RUNNING, TIME, POINTS, STOPS
    timer.stop()
    if RUNNING:
        if TIME % 10 == 0:
            POINTS += 1
        STOPS += 1
    RUNNING = False

def reset():
    """Reset the timer."""
    global TIME, POINTS, STOPS
    stop()
    TIME = POINTS = STOPS = 0

def increment():
    """Event handler for timer."""
    global TIME, COLOUR
    TIME += 1
    COLOUR = "#%02X%02X%02X" % (colour_picker(), colour_picker(), colour_picker())

def draw(canvas):
    """Draw handler."""
    global TIME

    # draw score
    score_str = str(POINTS) + "/" + str(STOPS)
    score_width = frame.get_canvas_textwidth(score_str, SCORE_SIZE, FONT)
    canvas.draw_text(score_str, [300 - score_width - 10, 30], SCORE_SIZE, "White", FONT)

    # draw time
    time_str = format(TIME)
    time_width = frame.get_canvas_textwidth(time_str, TIME_SIZE, FONT)
    canvas.draw_text(time_str, [300 - time_width - 75, 100], TIME_SIZE, COLOUR, FONT)


def main():
    """Play the game."""
    global timer, frame

    # create frame
    frame = simplegui.create_frame("Stopwatch: The Game", 300, 200, 200)

    # register event handlers
    frame.set_draw_handler(draw)
    frame.add_button("Start", start)
    frame.add_button("Stop", stop)
    frame.add_button("Reset", reset)

    # start frame
    timer = simplegui.create_timer(100, increment)
    frame.start()

if __name__ == '__main__':
    main()
