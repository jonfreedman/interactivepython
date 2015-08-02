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


class ImageInfo(object):
    """Util class to store image information."""

    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        """Initialise an image, by default zero radius, non-animated with no lifespan."""
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        """Pixel co-ordinates for center of image."""
        return self.center

    def get_size(self):
        """Pixel width and height of image."""
        return self.size

    def get_radius(self):
        """Pixel radius of image."""
        return self.radius

    def get_lifespan(self):
        """Frame lifespace of image."""
        return self.lifespan

    def get_animated(self):
        """True if image is animated."""
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


class Game(object):
    """Game object."""

    def __init__(self, ship, max_rocks):
        """Initialise the game with a single ship."""
        self.ship = ship
        self.max_rocks = max_rocks
        self.rocks = set()
        self.missiles = set()
        self.explosions = set()
        self.score = 0
        self.lives = 3
        self.time = 0
        self.started = False

    def start(self):
        """Start the game."""
        self.score = 0
        self.lives = 3
        self.time = 0
        self.started = True
        soundtrack.play()

    def restart(self):
        """Restart the game."""
        self.ship.set_thrust(False)
        self.rocks = set()
        self.missiles = set()
        self.explosions = set()
        self.started = False
        soundtrack.rewind()

    def rock_spawner(self):
        """Timer handler that spawns a rock."""
        if self.started and len(self.rocks) < self.max_rocks:
            pos = (random.randrange(WIDTH), random.randrange(HEIGHT))
            if dist(self.ship.get_position(), pos) > (self.ship.get_radius() + asteroid_info.get_radius() + 50):
                vel = (random.randrange(100) / 100., random.randrange(100) / 100.)
                angle_vel = random.choice([.05, -.05])
                self.rocks.add(Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info))

    def keydown(self, key):
        """Keypress handler."""
        if key == self.ship.turn_clockwise_key:
            self.ship.set_angle_vel(.05)
        elif key == self.ship.turn_counterclockwise_key:
            self.ship.set_angle_vel(-.05)
        elif key == self.ship.thrust_key:
            self.ship.set_thrust(True)
        elif key == self.ship.shoot_key:
            self.missiles.add(GAME.ship.shoot())

    def keyup(self, key):
        """Keypress handler."""
        if key == self.ship.turn_clockwise_key or key == self.ship.turn_counterclockwise_key:
            self.ship.set_angle_vel(0)
        elif key == self.ship.thrust_key:
            self.ship.set_thrust(False)

    def click(self, pos):
        """Mouseclick handler."""
        center = [WIDTH / 2, HEIGHT / 2]
        size = splash_info.get_size()
        inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
        inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
        if (not self.started) and inwidth and inheight:
            self.start()

    def draw(self, canvas):
        """Draw handler."""
        # animate background
        self.time += 1
        wtime = (self.time / 4) % WIDTH
        center = debris_info.get_center()
        size = debris_info.get_size()
        canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
        canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

        canvas.draw_text("Score " + str(self.score) + " Lives " + str(self.lives), (10, 34), 24, "blue", "sans-serif")

        # draw ship and sprites
        self.ship.draw(canvas)
        self._draw_sprite_group(self.rocks, canvas)
        self._draw_sprite_group(self.missiles, canvas)
        self._draw_sprite_group(self.explosions, canvas)

        # update ship and sprites
        self.ship.update()

        # process state
        self.score += self._process_missile_collisions()

        if self._process_rock_collisions(self.ship):
            self.lives -= 1
            self.score -= 1

        if self.lives == 0:
            self.restart()

        if not self.started:
            canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                              splash_info.get_size())

    def _draw_sprite_group(self, sprites, canvas):
        """Draw a set of sprites and remove any which have elapsed their lifetime."""
        elapsed_lifetimes = set()
        for sprite in sprites:
            sprite.draw(canvas)
            if not sprite.update():
                elapsed_lifetimes.add(sprite)
        sprites.difference_update(elapsed_lifetimes)

    def _process_rock_collisions(self, entity):
        """Check for collisions, entity can only destroy a single rock."""
        for rock in self.rocks:
            if entity.collide(rock):
                self.rocks.remove(rock)
                self.explosions.add(Sprite(rock.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
                return True
        return False

    def _process_missile_collisions(self):
        """Check for collisions, a missile can only destroy a single rock."""
        missile_collisions = set()
        for missile in self.missiles:
            if self._process_rock_collisions(missile):
                missile_collisions.add(missile)
        self.missiles.difference_update(missile_collisions)
        return len(missile_collisions)


class Ship(object):
    """Ship class."""

    def __init__(self, pos, vel, angle, image, info, thrust_sound, turn_clockwise_key, turn_counterclockwise_key, thrust_key, shoot_key):
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
        self.turn_clockwise_key = turn_clockwise_key
        self.turn_counterclockwise_key = turn_counterclockwise_key
        self.thrust_key = thrust_key
        self.shoot_key = shoot_key

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
        vector = angle_to_vector(self.angle)
        cannon_pos = (self.pos[0] + (vector[0] * self.radius), self.pos[1] + (vector[1] * self.radius))
        missile_vel = (self.vel[0] + (vector[0] * 6), self.vel[1] + (vector[1] * 6))
        return Sprite(cannon_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)

    def get_position(self):
        """Ship position."""
        return self.pos

    def get_radius(self):
        """Ship radius."""
        return self.radius

    def collide(self, other):
        """True if the ship has collided with another object."""
        return dist(self.get_position(), other.get_position()) < (self.get_radius() + other.get_radius())

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


class Sprite(object):
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

    def get_position(self):
        """Sprite position."""
        return self.pos

    def get_radius(self):
        """Sprite radius."""
        return self.radius

    def collide(self, other):
        """True if the ship has collided with another object."""
        return dist(self.get_position(), other.get_position()) < (self.get_radius() + other.get_radius())

    def draw(self, canvas):
        """Draw the sprite."""
        draw_center = self.image_center
        if self.animated:
            draw_center = (self.image_center[0] + (self.image_size[0] * self.age), self.image_center[1])
        canvas.draw_image(self.image, draw_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        """Update sprite's state."""
        # move the sprite
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1] %= HEIGHT

        # rotate
        self.angle += self.angle_vel

        self.age += 1
        return self.age < self.lifespan

GAME = Game(Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound,
             simplegui.KEY_MAP['right'], simplegui.KEY_MAP['left'], simplegui.KEY_MAP['up'], simplegui.KEY_MAP['space']),
            12)


def main():
    """
    RiceRocks.

    .. _SimpleGUICS2Pygame:
       https://simpleguics2pygame.readthedocs.org
    """
    frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

    frame.set_draw_handler(GAME.draw)
    frame.set_keydown_handler(GAME.keydown)
    frame.set_keyup_handler(GAME.keyup)
    frame.set_mouseclick_handler(GAME.click)

    timer = simplegui.create_timer(1000.0, GAME.rock_spawner)

    timer.start()
    frame.start()


if __name__ == '__main__':
    main()
