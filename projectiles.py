import pygame
from math import sqrt
from entity import Entity
import entities

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Projectile(Entity):

    def __init__(self, ID, x, y):
        # stuff that needs to be set: health, size
        super().__init__(ID)
        self._x = x
        self._y = y
        self._hitbox = self._x

    def _move(self, screen, dt):
        # python pls don't be mad
        pass

    def on_screen(self, screen):
        screen_size = screen.get_size()
        return self._x + self._width > 0 and self._x < screen_size[0] and \
            self._y + self._height > 0 and self._y < screen_size[1] and \
            self._health > 0 and (int(self._x_speed) != 0 or int(self._y_speed) != 0)

    def update(self, screen, dt):
        self._move(screen, dt)

class StraightProjectile(Projectile):

    targets = False

    def __init__(self, ID, x, y, params):
        # to be passed: health, width, height, x_speed, y_speed
        super().__init__(ID, x, y)
        self._health = int(params[0])
        self._width = int(params[1])
        self._height = int(params[2])
        self._x_speed = int(params[3]) # in px/s
        self._y_speed = int(params[4])

    def _move(self, screen, dt):
        self._x += self._x_speed * dt
        self._y += self._y_speed * dt
        #pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)

class FallingProjectile(Projectile):

    targets = False

    def __init__(self, ID, x, y, direction, params):
        # to be passed: health, width, height, speed, gravity
        # gravity: px/s^2
        super().__init__(ID, x, y)
        self._health = int(params[0])
        self._width = int(params[1])
        self._height = int(params[2])
        self._x_speed = int(params[3]) # in px/s
        self._gravity = int(params[4])
        self._direction = direction
        self._y_speed = 0

    def _move(self, screen, dt):
        self._x += self._x_speed * dt * self._direction
        self._y += self._y_speed * dt + self._gravity * dt * dt / 2
        self._y_speed += self._gravity * dt
        #pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)

class TargetedProjectile(Projectile):

    targets = True

    def __init__(self, ID, x, y, params):
        super().__init__(ID, x, y)
        # to be passed: health, width, height, speed, target
        self._health = int(params[0])
        self._width = int(params[1])
        self._height = int(params[2])
        self._speed = int(params[3])
        target = params[4]

        if target is None: # garbage collect
            self._x_speed = 0
            self._y_speed = 0
        else:
            # direction math
            self_center = self.get_center()
            target_center = target.get_center()
            x_diff = target_center[0] - self_center[0]
            y_diff = target_center[1] - self_center[1]
            hyp = sqrt(x_diff**2 + y_diff**2)
            self._x_speed = self._speed * x_diff / hyp
            self._y_speed = self._speed * y_diff / hyp

    def _move(self, screen, dt):
        self._x += self._x_speed * dt
        self._y += self._y_speed * dt

entities.entity_types["Straight"] = StraightProjectile
entities.entity_types["Falling"] = FallingProjectile
entities.entity_types["Targeted"] = TargetedProjectile