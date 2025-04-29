# weapons.py

import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREY, RED
import random


class Bullet:
    """
    Represents a bullet fired by the player's ship.
    Handles the bullet's movement and rendering.
    """

    def __init__(self, position, angle):
        """
        Initializes the bullet with its position, velocity, and direction.

        Args:
            position (tuple): The starting position of the bullet (x, y).
            angle (float): The angle at which the bullet is fired.
        """
        self.image = pygame.Surface((4, 4))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=position)
        self.velocity = (
            pygame.math.Vector2(
                math.cos(math.radians(angle)), math.sin(math.radians(angle))
            )
            * 5
        )  # Bullet speed

    def update(self):
        """Updates the bullet's position based on its velocity."""
        self.rect.center += self.velocity

        # Remove the bullet if it goes off-screen
        if not (
            0 <= self.rect.centerx <= SCREEN_WIDTH
            and 0 <= self.rect.centery <= SCREEN_HEIGHT
        ):
            return False
        return True

    def draw(self, surface):
        """
        Draws the bullet onto the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the bullet on.
        """
        surface.blit(self.image, self.rect.topleft)


class Homing_Bullet(Bullet):
    """
    Represents a homing bullet fired by the player's ship.
    Handles the bullet's movement and rendering, and tracks onto the nearest Rock object.
    """

    def __init__(self, position, angle, rocks):
        """
        Initializes the homing bullet with its position, velocity, and direction.

        Args:
            position (tuple): The starting position of the bullet (x, y).
            angle (float): The angle at which the bullet is fired.
            rocks (list[Rock]): A list of Rock objects to track onto.
        """
        super().__init__(position, angle)
        self.rocks = rocks
        self.target = None

    def update(self):
        if self.target is None or self.target.size <= 0:
            self.target = self._find_nearest_rock()
        if self.target is not None:
            self._turn_towards_target()
        return super().update()

    def _find_nearest_rock(self):
        """Finds the nearest Rock object to the homing bullet."""
        nearest_rock = None
        nearest_distance = float("inf")
        for rock in self.rocks:
            distance = math.hypot(
                self.rect.centerx - rock.rect.centerx,
                self.rect.centery - rock.rect.centery,
            )
            if distance < nearest_distance:
                nearest_rock = rock
                nearest_distance = distance
        return nearest_rock

    def _turn_towards_target(self):
        """Updates the homing bullet's velocity to turn towards its target."""
        if self.target is not None:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            angle = math.atan2(dy, dx)
            self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * 5


class Circle_Bullet(Bullet):
    """
    Represents a bullet that travels in a continuous circle around the ship.
    """

    def __init__(self, position, angle, ship):
        """
        Initializes the circle bullet with its position, velocity, and the ship it orbits.
        """
        super().__init__(position, angle)
        self.ship = ship
        self.radius = 50
        self.angle = angle
        self.color = (75, 0, 130)  # Purple
        self.speed = 2

    def update(self):
        """
        Updates the circle bullet's position in a continuous circle around the ship.
        """
        self.angle += self.speed
        self.rect.centerx = (
            self.ship.rect.centerx + math.cos(math.radians(self.angle)) * self.radius
        )
        self.rect.centery = (
            self.ship.rect.centery + math.sin(math.radians(self.angle)) * self.radius
        )
        return True

    def draw(self, surface):
        """
        Draws the circle bullet onto the given surface.
        """
        pygame.draw.circle(surface, self.color, self.rect.center, 3)

class Cluster_Bomb(Bullet):
    """
    Represents a bullet that explodes into multiple homing bullets when it reaches its destination.
    """

    def __init__(self, position, angle, rocks):
        """
        Initializes the cluster bomb with its position, velocity, and direction.
        """
        super().__init__(position, angle)
        self.image = pygame.Surface((4, 4))
        self.image.fill((0, 0, 255))  # Blue
        self.rect = self.image.get_rect(center=position)
        self.velocity = pygame.math.Vector2(
            math.cos(math.radians(angle)), math.sin(math.radians(angle))
        ) * 5
        self.wait_time = 50  # Wait 50 frames before exploding
        self.num_bullets = 5  # Explode into 5 homing bullets
        self.rocks = rocks

    def update(self):
        """
        Updates the cluster bomb's position and explodes it when it reaches its destination.
        """
        self.rect.center += self.velocity
        self.wait_time -= 1
        if self.wait_time <= 0:
            bullets = []
            for _ in range(self.num_bullets):
                angle = random.uniform(0, 360)
                bullets.append(Homing_Bullet(self.rect.center, angle, self.rocks))
            self.wait_time = 50
            return bullets
        return []

    def draw(self, surface):
        """
        Draws the cluster bomb onto the given surface.
        """
        surface.blit(self.image, self.rect.topleft)
