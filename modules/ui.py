# modules/ui.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class HealthBar:
    def __init__(self, max_health=100, current_health=100):
        """
        Initializes the health bar.

        :param max_health: The maximum health value.
        :param current_health: The current health value.
        """
        self.max_health = max_health
        self.current_health = current_health

        try:
            self.background = pygame.image.load("assets/img/ui/health_bar.png").convert_alpha()
            self.background = pygame.transform.scale(self.background, (200, 20))
            self.foreground = pygame.image.load("assets/img/ui/health_foreground.png").convert_alpha()
            self.foreground = pygame.transform.scale(self.foreground, (200, 20))
        except pygame.error as e:
            print(f"Error loading health bar images: {e}")
            sys.exit()

    def update(self, damage):
        """
        Updates the current health based on damage taken.

        :param damage: The amount of damage taken.
        """
        self.current_health = max(0, self.current_health - damage)

    def draw(self, surface):
        """
        Draws the health bar on the screen.

        :param surface: Pygame surface to draw on.
        """
        surface.blit(self.background, (10, 10))
        health_ratio = self.current_health / self.max_health
        foreground_width = int(200 * health_ratio)
        foreground_scaled = pygame.transform.scale(self.foreground, (foreground_width, 20))
        surface.blit(foreground_scaled, (10, 10))
