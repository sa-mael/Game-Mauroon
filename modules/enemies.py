# modules/enemies.py

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_SIZE

class Enemy:
    def __init__(self, x, y, image_path, speed=50):
        """
        Initializes an enemy.

        :param x: X position of the enemy.
        :param y: Y position of the enemy.
        :param image_path: Path to the enemy's image.
        :param speed: Movement speed of the enemy.
        """
        self.grid_x = x
        self.grid_y = y
        self.speed = speed

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        except pygame.error as e:
            print(f"Error loading enemy image '{image_path}': {e}")
            sys.exit()

    def move_towards_player(self, player, dt):
        """
        Moves the enemy towards the player.

        :param player: Player object.
        :param dt: Delta time (seconds).
        """
        dx = player.grid_x - self.grid_x
        dy = player.grid_y - self.grid_y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.grid_x += (dx / distance) * self.speed * dt
            self.grid_y += (dy / distance) * self.speed * dt

    def draw(self, surface, camera):
        """
        Draws the enemy on the screen with camera offset.

        :param surface: Pygame surface to draw on.
        :param camera: Camera object for offset.
        """
        iso_x = (self.grid_x - self.grid_y) * 22 * SCALE_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * 22 * SCALE_SIZE // 4 + SCREEN_HEIGHT // 3.5

        # Camera offset
        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - 20  # 20 is half the enemy width
        draw_y = iso_y + camera.offset_y - 20  # 20 is half the enemy height

        surface.blit(self.image, (draw_x, draw_y))
