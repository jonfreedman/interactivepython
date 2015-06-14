"""Mini-Project: Week 3."""

from __future__ import print_function
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'


class Timer(object):

    """Keeps track of time."""

    def __init__(self):
        """Create new timer at 0."""
        self.time = 0
        self.points = 0
        self.stops = 0
        self.running = False
        self.colour = "#FFFFFF"

    def set_timer(self, timer):
        """Pass reference to simplegui timer.

        :param timer: simplegui timer
        """
        self.timer = timer

    def reset(self):
        """Reset timer to 0."""
        self.time = 0
        self.points = 0
        self.stops = 0
        self.running = False
        self.colour = "#FFFFFF"
        self.timer.stop()

    def start(self):
        """Start timer."""
        self.running = True
        self.timer.start()

    def stop(self):
        """Stop timer."""
        self.timer.stop()
        if self.running:
            if self.time % 10 == 0:
                self.points += 1
            self.stops += 1
        self.running = False

    def tick(self):
        """Tick the timer."""
        self.time += 1
        self.colour = "#%02X%02X%02X" % (self.__colour_picker(), self.__colour_picker(), self.__colour_picker())

    def __colour_picker(self):
        """Generate a random 2-digit hex pastel colour."""
        return (255 + random.randrange(0, 256)) / 2


# define global variables
TIME = Timer()
FONT = "monospace"
SCORE_SIZE = 24
TIME_SIZE = 36


def format(t):
    """Convert time in tenths of a second into a formatted string A:BC.D."""
    mins = "%d" % (t // 600)
    secs = "%02d" % ((t // 10) % 60)
    tenths = "%d" % (t % 10)
    return mins + ":" + secs + "." + tenths


def draw(frame, canvas):
    """Draw handler."""
    # draw score
    score_str = str(TIME.points) + "/" + str(TIME.stops)
    score_width = frame.get_canvas_textwidth(score_str, SCORE_SIZE, FONT)
    canvas.draw_text(score_str, [300 - score_width - 10, 30], SCORE_SIZE, "White", FONT)
    # draw time
    time_str = format(TIME.time)
    time_width = frame.get_canvas_textwidth(time_str, TIME_SIZE, FONT)
    canvas.draw_text(time_str, [300 - time_width - 75, 100], TIME_SIZE, TIME.colour, FONT)


def main():
    """
    Stopwatch: The Game.

    Stop the timer to the second exactly to score a point

    Timer colours courtesy of http://tinyurl.com/mopmdyn

    .. _SimpleGUICS2Pygame:
       https://simpleguics2pygame.readthedocs.org
    """

    # create frame
    frame = simplegui.create_frame("Stopwatch: The Game", 300, 200, 200)

    # register event handlers
    draw_handler = lambda h, f, c: h(f, c)
    frame.set_draw_handler(lambda c: draw_handler(draw, frame, c))
    frame.add_button("Start", TIME.start)
    frame.add_button("Stop", TIME.stop)
    frame.add_button("Reset", TIME.reset)

    # start frame
    TIME.set_timer(simplegui.create_timer(100, TIME.tick))
    frame.start()


if __name__ == '__main__':
    main()
