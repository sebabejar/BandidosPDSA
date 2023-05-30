from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import get_random_velocity, load_sprite, wrap_position

UP = Vector2(0, -1)
QPOS = Vector2(-0.85, -0.5)
WPOS = Vector2(-0.63, -0.78)
EPOS = Vector2(0.59, -0.81)
RPOS = Vector2(0.78, -0.63)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 15

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback

        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite("Gun"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
        print(self.direction)
    def rotate1(self, position):
        if(position == 1):
            self.direction.update(QPOS)
            print(1)
        elif(position == 2):
            self.direction.update(WPOS)
            print(2)
        elif(position == 3):
            self.direction.update(EPOS)
            print(3)
        elif(position == 4):
            self.direction.update(RPOS)
            print(4)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)


class Bandido(GameObject):
    def __init__(self, position, create_bandido_callback, size=3):
        self.create_bandido_callback = create_bandido_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("Sprite"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(0, 0))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                bandido = Bandido(
                    self.position, self.create_bandido_callback, self.size - 1
                )
                self.create_bandido_callback(bandido)


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("Bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
