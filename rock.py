# rock.py

import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREY

class Rock:
    """
    Represents a fragmentable rock in the game.
    Handles the rock's movement, splitting, and rendering.
    """

    def __init__(self, position=None, size=40):
        """
        Initializes the rock with a random position, velocity, and size.

        Args:
            position (tuple): The starting position of the rock (x, y). If None, a random position is used.
            size (int): The size of the rock. Defaults to 40.
        """
        self.size = size
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREY, (self.size // 2, self.size // 2), self.size // 2)
        self.rect = self.image.get_rect(center=position or (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed

    def update(self):
        """Updates the rock's position based on its velocity."""
        self.rect.center += self.velocity
        self.rect.centerx %= SCREEN_WIDTH
        self.rect.centery %= SCREEN_HEIGHT

    def draw(self, surface):
        """
        Draws the rock onto the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the rock on.
        """
        surface.blit(self.image, self.rect.topleft)

    def split(self):
        """
        Splits the rock into smaller fragments if its size is above a certain threshold.

        Returns:
            list[Rock]: A list of new Rock objects representing the fragments.
        """
        if self.size > 20:
            return [
                Rock(position=self.rect.center, size=self.size // 2),
                Rock(position=self.rect.center, size=self.size // 2)
            ]
        else:
            return []  # No fragments if the rock is too small
