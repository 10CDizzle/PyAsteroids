# ship.py

import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SHIP_SPEED, SHIP_ROTATION_SPEED

class Ship:
    """
    Represents the player's ship in the game.
    Handles the ship's movement, rotation, and drawing with pre-rendered rotations.
    """

    def __init__(self):
        """Initializes the ship with its shape, position, velocity, and pre-rendered rotations."""
        # Create the ship's image with the triangle pointing upwards
        self.original_image = pygame.Surface((13, 13), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (255, 255, 255), [(13, 6), (0, 0), (0, 13)])

        # Pre-render the rotated images
        self.pre_rendered_rotations = []
        self.pre_render_rotations()

        self.rect = self.original_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.angle_index = 0
        self.velocity = pygame.math.Vector2(0, 0)

    def pre_render_rotations(self):
        """Pre-renders the ship's image at different angles and stores them in a list."""
        for angle in range(0, 360, SHIP_ROTATION_SPEED):
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            self.pre_rendered_rotations.append(rotated_image)

    def rotate(self, direction):
        """
        Rotates the ship by updating the angle index based on the direction.

        Args:
            direction (int): The direction to rotate the ship, either 1 (clockwise) or -1 (counterclockwise).
        """
        self.angle_index = (self.angle_index + direction) % len(self.pre_rendered_rotations)

    def accelerate(self):
        """Accelerates the ship in the direction it is facing."""
        angle = -self.angle_index * SHIP_ROTATION_SPEED
        self.velocity += pygame.math.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * SHIP_SPEED

    def update(self):
        """Updates the ship's position based on its velocity and ensures it stays within the screen bounds."""
        self.rect.center += self.velocity
        self.rect.centerx %= SCREEN_WIDTH
        self.rect.centery %= SCREEN_HEIGHT

    def draw(self, surface):
        """
        Draws the ship onto the given surface using the pre-rendered image based on the current rotation.

        Args:
            surface (pygame.Surface): The surface to draw the ship on.
        """
        current_image = self.pre_rendered_rotations[self.angle_index]
        rotated_rect = current_image.get_rect(center=self.rect.center)
        surface.blit(current_image, rotated_rect.topleft)
