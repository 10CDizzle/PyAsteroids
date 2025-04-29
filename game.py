# game.py

import pygame
from ship import Ship
from weapons import Bullet, Homing_Bullet, Circle_Bullet, Cluster_Bomb
from rock import Rock
from score import Score
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, SHIP_ROTATION_SPEED
import random


class Game:
    """
    Manages the main game loop, title screen, and game state.
    """

    def __init__(self):
        """Initializes the game, including setting up the screen, clock, player's ship, bullets, rocks, and score."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids Clone")
        self.clock = pygame.time.Clock()
        self.ship = Ship()
        self.bullets = []  # List to store active bullets
        self.rocks = []  # List to store active rocks
        self.score = Score()  # Initialize the score
        self.rock_spawn_timer = 0  # Timer to control rock spawning

    def title_screen(self):
        """Displays the title screen and waits for the player to press a key to start the game."""
        font = pygame.font.Font(None, 74)
        text = font.render("Asteroids Clone", True, WHITE)
        self.screen.blit(
            text,
            (
                SCREEN_WIDTH // 2 - text.get_width() // 2,
                SCREEN_HEIGHT // 2 - text.get_height() // 2,
            ),
        )

        font = pygame.font.Font(None, 36)
        text = font.render("Press any key to start", True, WHITE)
        self.screen.blit(
            text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 50)
        )

        pygame.display.flip()

        # Wait for the player to press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def spawn_rock(self):
        """Spawns a new rock at a random location on the screen."""
        rock = Rock(size=random.randint(10, 200))
        self.rocks.append(rock)

    def check_collisions(self):
        """Checks for collisions between bullets, rocks, and the ship."""
        # Check bullet and rock collisions
        for bullet in self.bullets[:]:
            for rock in self.rocks[:]:
                if bullet.rect.colliderect(rock.rect):
                    self.bullets.remove(bullet)
                    fragments = rock.split()
                    self.rocks.remove(rock)
                    self.rocks.extend(fragments)
                    self.score.increase(10)  # Increase score when a rock is destroyed

                    # Draw an orange sphere to represent an explosion
                    pygame.draw.circle(self.screen, (255, 165, 0), rock.rect.center, 10)
                    pygame.display.update()
                    pygame.time.wait(10)  # Pause for 100 ms to show the explosion
                    break

        # Check ship and rock collisions
        for rock in self.rocks:
            if self.ship.rect.colliderect(rock.rect):
                print("Ship hit! Game over.")
                pygame.quit()
                exit()

    def main_game(self):
        """Runs the main game loop, handling events, updating the game state, and drawing the screen."""
        running = True

        # Generate a random star pattern
        star_pattern = []
        for _ in range(50):
            star_pattern.append(
                (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            )

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.ship.rotate(1)  # Rotate counterclockwise
            if keys[pygame.K_RIGHT]:
                self.ship.rotate(-1)  # Rotate clockwise
            if keys[pygame.K_UP]:
                self.ship.accelerate()
            if keys[pygame.K_SPACE]:
                # Fire a bullet when spacebar is pressed
                bullet = Bullet(
                    self.ship.rect.center, -self.ship.angle_index * SHIP_ROTATION_SPEED
                )
                self.bullets.append(bullet)
            # if the h key is pressed, spawn a homing bullet
            if keys[pygame.K_h]:
                bullet = Homing_Bullet(
                    self.ship.rect.center,
                    -self.ship.angle_index * SHIP_ROTATION_SPEED,
                    self.rocks,
                )
                self.bullets.append(bullet)
            if keys[pygame.K_j]:
                bullet = Circle_Bullet(
                    self.ship.rect.center,
                    -self.ship.angle_index * SHIP_ROTATION_SPEED,
                    self.ship,
                )
                self.bullets.append(bullet)
            if keys[pygame.K_k]:
                bullet = Cluster_Bomb(
                    self.ship.rect.center,
                    -self.ship.angle_index * SHIP_ROTATION_SPEED, self.rocks
                )
                self.bullets.append(bullet)

            self.ship.update()

            # Update and draw bullets
            for bullet in self.bullets[:]:
                if not bullet.update():
                    self.bullets.remove(bullet)

            # Spawn rocks at intervals
            self.rock_spawn_timer += 1
            if self.rock_spawn_timer > 120:  # Adjust spawn interval here
                self.spawn_rock()
                self.rock_spawn_timer = 0

            # Update rocks
            for rock in self.rocks:
                rock.update()

            # Check collisions
            self.check_collisions()

            # Draw everything
            self.screen.fill(BLACK)
            for star in star_pattern:
                pygame.draw.rect(self.screen, WHITE, (star[0], star[1], 2, 2))
            self.ship.draw(self.screen)
            for bullet in self.bullets:
                bullet.draw(self.screen)
            for rock in self.rocks:
                rock.draw(self.screen)
            self.score.draw(self.screen)  # Draw the score
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def run(self):
        """Runs the game, starting with the title screen."""
        self.title_screen()
        self.main_game()
