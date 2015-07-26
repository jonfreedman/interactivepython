"""Mini-Project: Week 3-4."""

from __future__ import print_function
import random
import math

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'jon'

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


class Ship(object):
    """Ship class."""

    def __init__(self, pos, vel, angle, image, info, thrust_sound):
        """Spawn a ship."""
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrust_sound = thrust_sound

    def set_angle_vel(self, angle):
        """Set the angle velocity of the ship to control rotation."""
        self.angle_vel = angle

    def set_thrust(self, thrust):
        """Turn the ships thrusters on/off."""
        self.thrust = thrust
        if thrust:
            self.thrust_sound.play()
        else:
            self.thrust_sound.rewind()

    def shoot(self):
        """Shoot a missile."""
        global a_missile
        vector = angle_to_vector(self.angle)
        cannon_pos = (self.pos[0] + (vector[0] * 40), self.pos[1] + (vector[1] * 40))
        missile_vel = (self.vel[0] + (vector[0] * 2), self.vel[1] + (vector[1] * 2))
        a_missile = Sprite(cannon_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)

    def draw(self, canvas):
        """Draw the ship."""
        if self.thrust:
            thrust_center = (self.image_center[0] + self.image_size[0], self.image_center[1])
            canvas.draw_image(self.image, thrust_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        """Update ship's state."""
        # move the ship
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1] %= HEIGHT

        # apply friction
        self.vel[0] *= .99
        self.vel[1] *= .99

        # adjust thrust
        self.angle += self.angle_vel
        forward_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward_vector[0] * .1
            self.vel[1] += forward_vector[1] * .1


class Sprite:
    """Sprite class."""

    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        """Spawn a sprite."""
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        """Draw the sprite."""
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        """Update sprite's state."""
        # move the sprite
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1] %= HEIGHT

        # rotate
        self.angle += self.angle_vel


def draw(canvas):
    """Draw handler."""
    global time

    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text("Score " + str(score) + " Lives " + str(lives), (10, 34), 24, "blue", "sans-serif")

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()


def keydown(key):
    """Keypress handler."""
    if key == simplegui.KEY_MAP['left']:
        my_ship.set_angle_vel(-.05)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.set_angle_vel(.05)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()


def keyup(key):
    """Keypress handler."""
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)


def rock_spawner():
    """Timer handler that spawns a rock."""
    global a_rock
    pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
    vel = (random.randrange(100) / 100., random.randrange(100) / 100.)
    angle_vel = random.choice([.05, -.05])
    a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0, missile_image, missile_info, missile_sound)


def main():
    """
    RiceRocks.

    .. _SimpleGUICS2Pygame:
       https://simpleguics2pygame.readthedocs.org
    """
    frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)

    timer = simplegui.create_timer(1000.0, rock_spawner)

    timer.start()
    frame.start()


if __name__ == '__main__':
    main()
