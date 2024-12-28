# modules/player.py
import pygame
import sys
from modules.config import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y, layer=1, speed=10, texture_path="assets/img/blocks/player.png"):
        """
        :param x, y: starting tile coordinates in grid space
        :param layer: which layer of the world
        :param speed: movement speed
        :param texture_path: path to player sprite
        """
        self.grid_x = x
        self.grid_y = y
        self.layer = layer
        self.speed = speed

        # Load player texture
        try:
            image = pygame.image.load(texture_path).convert_alpha()
            self.texture = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
        except pygame.error as e:
            print(f"Error loading player texture '{texture_path}': {e}")
            sys.exit()

    def move(self, dx, dy, dt, world):
        new_x = self.grid_x + dx * self.speed * dt
        new_y = self.grid_y + dy * self.speed * dt
    
        # Convert to int for checking collisions on the tile grid
        int_new_x = int(new_x)
        int_new_y = int(new_y)
    
        from modules.config import SOLID_BLOCKS  # or pass it in some way
    
        if world.is_position_walkable(self.layer, int_new_x, int_new_y, SOLID_BLOCKS):
            self.grid_x = new_x
            self.grid_y = new_y
        else:
            # Collided with a solid block – do not update position
            pass

    def jump(self, direction, world):
        """Jump between layers, if within bounds."""
        int_x = int(self.grid_x)
        int_y = int(self.grid_y)

        if direction == "up" and self.layer > 0:
            self.layer -= 1
        elif direction == "down" and self.layer < (world.layers - 1):
            self.layer += 1

    def draw(self, surface, camera):
        """
        Convert (grid_x, grid_y) to isometric and draw the player.
        """
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE // 4 - self.layer * BLOCK_SIZE // 2

        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - BLOCK_SIZE // 2
        draw_y = iso_y + int(SCREEN_HEIGHT // 3.5) + camera.offset_y - BLOCK_SIZE // 2

        surface.blit(self.texture, (draw_x, draw_y))
