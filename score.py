# score.py

import pygame
from settings import WHITE

class Score:
    """
    Manages the player's score and its display on the screen.
    """
    
    def __init__(self):
        """Initializes the score with zero and sets up the font for display."""
        self.score = 0
        self.font = pygame.font.Font(None, 36)
    
    def increase(self, amount):
        """
        Increases the score by a specified amount.

        Args:
            amount (int): The amount to increase the score by.
        """
        self.score += amount
    
    def draw(self, surface):
        """
        Draws the current score on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the score on.
        """
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
