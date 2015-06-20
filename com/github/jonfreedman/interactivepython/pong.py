"""Mini-Project: Week 4."""

from __future__ import print_function
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'


class Drawable(object):
    """Drawable base class."""

    def __init__(self, position):
        """Record initial and current position."""
        self.initial_position = tuple(position)
        self.position = position

    def get_x(self):
        """x co-ordinate."""
        return int(self.position[0])

    def get_y(self):
        """y co-ordinate."""
        return int(self.position[1])

    def reset(self):
        """Reset to initial position."""
        self.position = list(self.initial_position)


class Ball(Drawable):
    """Class to encapsulate translation from velocity in pixels per second to position refreshed 60 times per sec."""

    def __init__(self, position, radius):
        """Initialise with 0 velocity."""
        Drawable.__init__(self, position)
        self.radius = radius
        self.velocity = [0, 0]
        self.direction = LEFT
        self.colour = GREYS

    def move(self):
        """Move according to current velocity."""
        self.position[0] += self.velocity[0] / 60.
        self.position[1] += self.velocity[1] / 60.

    def bounce_horizontal(self):
        """Bounce horizontally off a vertical surface."""
        self.velocity[0] *= -1.1
        self.position[0] += self.velocity[0] / 60.
        self.direction = not self.direction

    def bounce_vertical(self):
        """Bounce vertically off a horizontal surface."""
        self.velocity[1] *= -1
        self.position[1] += self.velocity[1] / 60.

    def freeze(self):
        """Set velocity to zero and turn red."""
        self.velocity = [0, 0]
        self.colour = REDS

    def reset(self, direction=None):
        """Return to original position and set a random velocity."""
        Drawable.reset(self)
        if direction is None:
            direction = not self.direction
        self.velocity = [(-1 if direction == LEFT else 1) * random.randrange(120, 240), -random.randrange(60, 180)]
        self.direction = direction
        self.colour = GREYS

    def draw(self, canvas):
        """Draw self."""
        centre = (self.get_x(), self.get_y())
        canvas.draw_circle(centre, self.radius, 1, self.colour[0], self.colour[1])
        canvas.draw_circle(centre, self.radius * (5 / 6.), 1, self.colour[2], self.colour[2])
        canvas.draw_circle(centre, self.radius * (4 / 6.), 1, self.colour[3], self.colour[3])
        canvas.draw_circle(centre, self.radius * (3 / 6.), 1, self.colour[4], self.colour[4])
        canvas.draw_circle(centre, self.radius * (2 / 6.), 1, self.colour[5], self.colour[5])
        canvas.draw_circle(centre, self.radius * (1 / 6.), 1, self.colour[6], self.colour[6])


class Paddle(Drawable):
    """Represents the paddles controlled by players."""

    def __init__(self, position, height, width, vertical_range):
        """Initialise with 0 velocity."""
        Drawable.__init__(self, position)
        self.height = height
        self.width = width
        self.velocity = 0
        self.vertical_range = vertical_range

    def move(self):
        """Move according to current velocity."""
        self.position[1] += self.velocity / 60.
        if not self.__within_vertical_range():
            self.position[1] -= self.velocity / 60.
            self.velocity = 0

    def change_velocity(self, velocity):
        """Change velocity."""
        if self.__within_vertical_range():
            self.velocity = velocity

    def touching_ball(self, ball):
        """Check if touching a given ball."""
        return ((ball.get_y() >= self.get_y() - (self.height / 2.)) and
                (ball.get_y() <= self.get_y() + (self.height / 2.) - 1))

    def __within_vertical_range(self):
        """Check within permitted vertical range."""
        return not ((self.get_y() - (self.height / 2.) < self.vertical_range[0]) or
                    (self.get_y() + (self.height / 2.) > self.vertical_range[1]))

    def reset(self):
        """Return to original position and set velocity to zero."""
        Drawable.reset(self)
        self.velocity = 0

    def draw(self, canvas):
        """Draw self."""
        _x1 = self.position[0] - (self.width / 2)
        _x2 = self.position[0] + (self.width / 2)
        _y1 = self.position[1] - (self.height / 2)
        _y2 = self.position[1] + (self.height / 2)
        canvas.draw_polygon([(_x1, _y1), (_x1, _y2), (_x2, _y2), (_x2, _y1)], 1, "white", "white")

# initialize globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
LEFT = False
RIGHT = True
GREYS = ["#657382", "#708090", "#7E8D9B", "#8D99A6", "#9BA6B1", "#A9B3BC", "#B8C0C8"]
REDS = ["#991F00", "#B22400", "#CC2900", "#E62E00", "#FF3300", "#FF4719", "#FF5C33"]

PAUSE = 20
SCORES = [0, 0]
BALL = Ball([WIDTH / 2., HEIGHT / 2.], 20)
PADDLE1 = Paddle([PAD_WIDTH / 2, HEIGHT / 2], PAD_HEIGHT, PAD_WIDTH, (0, HEIGHT - 1))
PADDLE2 = Paddle([WIDTH - PAD_WIDTH / 2, HEIGHT / 2], PAD_HEIGHT, PAD_WIDTH, (0, HEIGHT - 1))
DRAWABLE = [BALL, PADDLE1, PADDLE2]


def new_game():
    """Start a new game."""
    SCORES[0] = 0
    SCORES[1] = 0
    BALL.reset(random.choice([LEFT, RIGHT]))
    PADDLE1.reset()
    PADDLE2.reset()


def draw(canvas):
    """Draw handler."""
    global PAUSE

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    if PAUSE > 1:
        PAUSE -= 1
    elif PAUSE == 1:
        BALL.reset()
        PAUSE -= 1
    else:
        # update ball/paddles
        for drawable in DRAWABLE:
            drawable.move()

        # check if top or bottom walls hit
        if (BALL.get_y() <= BALL_RADIUS) or (BALL.get_y() >= HEIGHT - BALL_RADIUS - 1):
            BALL.bounce_vertical()

        # check for gutter/paddles hit
        hit_left = BALL.get_x() <= BALL_RADIUS + PAD_WIDTH
        hit_right = BALL.get_x() >= WIDTH - BALL_RADIUS - PAD_WIDTH - 1
        if hit_left or hit_right:
            if (hit_left and PADDLE1.touching_ball(BALL)) or (hit_right and PADDLE2.touching_ball(BALL)):
                # hit the ball
                BALL.bounce_horizontal()
            else:
                # missed the ball, assign a point
                if LEFT == BALL.direction:
                    SCORES[1] += 1
                else:
                    SCORES[0] += 1
                BALL.freeze()
                PAUSE = 20

    # draw ball/paddles
    for drawable in DRAWABLE:
        drawable.draw(canvas)

    # draw scores
    canvas.draw_text(str(SCORES[0]), (100, 50), 24, "white", "monospace")
    canvas.draw_text(str(SCORES[1]), (WIDTH - 100, 50), 24, "white", "monospace")


def keydown(key):
    """Keypress handler."""
    if key == simplegui.KEY_MAP['down']:
        PADDLE2.change_velocity(360)
    elif key == simplegui.KEY_MAP['up']:
        PADDLE2.change_velocity(-360)
    elif key == simplegui.KEY_MAP['s']:
        PADDLE1.change_velocity(360)
    elif key == simplegui.KEY_MAP['w']:
        PADDLE1.change_velocity(-360)


def keyup(key):
    """Keypress handler."""
    if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['up']:
        PADDLE2.velocity = 0
    elif key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['w']:
        PADDLE1.velocity = 0


def main():
    """
    Pong.

    .. _SimpleGUICS2Pygame:
       https://simpleguics2pygame.readthedocs.org
    """
    frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    frame.add_button("Restart", new_game)

    new_game()
    frame.start()


if __name__ == '__main__':
    main()
