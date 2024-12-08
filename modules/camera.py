# camera.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, scale_size):
        self.scale_size = scale_size
        self.offset_x = 0
        self.offset_y = 0

    def update(self, player):
        # Center the camera on the player
        self.offset_x = SCREEN_WIDTH // 2 - player.x * self.scale_size
        self.offset_y = SCREEN_HEIGHT // 2 - player.y * self.scale_size

    def apply_zoom(self, scale_factor):
        self.scale_size *= scale_factor
