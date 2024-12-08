# world.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class World:
    def __init__(self):
        self.map_data = self.load_map()

    def load_map(self):
        # Simulate loading map data (should load from a file)
        return [
            [1, 1, 1,2,2,2,2,2,2,2,],
            [2, 3, 1,1,1,1,1,1,1],
            [1, 1, 1,1,1,1,1,1,]
        ]

    def render(self, surface, textures, camera):
        for y, row in enumerate(self.map_data):
            for x, block_id in enumerate(row):
                block_image = textures.get(str(block_id), None)
                if block_image:
                    # Calculate block position on the screen
                    iso_x = (x - y) * 32 * camera.scale_size
                    iso_y = (x + y) * 16 * camera.scale_size - camera.offset_y
                    surface.blit(block_image, (iso_x + camera.offset_x, iso_y))
