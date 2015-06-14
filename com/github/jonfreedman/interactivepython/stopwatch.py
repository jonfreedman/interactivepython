"""
Stopwatch: The Game

Stop the timer to the second exactly to score a point

Timer colours courtesy of http://tinyurl.com/mopmdyn

.. _SimpleGUICS2Pygame:
   https://simpleguics2pygame.readthedocs.org
"""

__author__ = 'jon'

import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# define global variables
time = 0
colour = "#FFFFFF"
running = False
points = 0
stops = 0

font = "monospace"
score_size = 24
time_size = 36

def format(t):
    """Convert time in tenths of a second into a formatted string A:BC.D"""
    mins = "%d" % (t // 600)
    secs = "%02d" % ((t // 10) % 60)
    tenths = "%d" % (t % 10)
    return mins + ":" + secs + "." + tenths

def colour_picker():
    return (255 + random.randrange(0, 256)) / 2

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer, running
    timer.start()
    running = True

def stop():
    global timer, running, time, points, stops
    timer.stop()
    if running:
        if time % 10 == 0:
            points += 1
        stops += 1
    running = False

def reset():
    global time, points, stops
    stop()
    time = points = stops = 0

def increment():
    """event handler for timer"""
    global time, colour
    time += 1
    colour = "#%02X%02X%02X" % (colour_picker(), colour_picker(), colour_picker())

# define draw handler
def draw(canvas):
    global time

    # draw score
    score_str = str(points) + "/" + str(stops)
    score_width = frame.get_canvas_textwidth(score_str, score_size, font)
    canvas.draw_text(score_str, [300 - score_width - 10, 30], score_size, "White", font)

    # draw time
    time_str = format(time)
    time_width = frame.get_canvas_textwidth(time_str, time_size, font)
    canvas.draw_text(time_str, [300 - time_width - 75, 100], time_size, colour, font)


def main():
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