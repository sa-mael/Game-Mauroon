# modules/player.py

import pygame
import sys

from modules.config import PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y, layer=8, speed=10, texture_path="assets/img/blocks/player.png"):
        """
        :param x, y: starting tile coordinates in grid space
        :param layer: which layer of the world
        :param speed: movement speed
        :param texture_path: path to player sprite
        """

from modules.config import PLAYER_SIZE, BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    """
    Manages the player's position, movement, layer, and drawing.
    """
    def __init__(self, x, y, layer, speed, texture_path="assets/img/blocks/player.png"):

        self.grid_x = x
        self.grid_y = y
        self.layer = layer
        self.speed = speed  # number of tiles per second (or however you interpret "speed")

        # Load the player sprite
        try:
            image = pygame.image.load(texture_path).convert_alpha()
            self.texture = pygame.transform.scale(image, (PLAYER_SIZE, PLAYER_SIZE))

            self.texture = pygame.image.load(texture_path).convert_alpha()
            # Scale to your desired size
            self.texture = pygame.transform.scale(self.texture, (PLAYER_SIZE, PLAYER_SIZE))

        except pygame.error as e:
            print(f"Error loading player texture '{texture_path}': {e}")
            sys.exit()

    def move(self, dx, dy, dt, world):
        """
        Moves the player in the grid, checking collisions:
          - We compute a proposed new (x, y) in the grid.
          - We ensure that tile is valid (i.e., block != 0).
        """
        new_x = self.grid_x + dx * self.speed * dt
        new_y = self.grid_y + dy * self.speed * dt

        # We'll check collisions by looking at the integer tile coords.
        int_x = int(new_x)
        int_y = int(new_y)

        # Basic boundary checks
        if self.layer < 0 or self.layer >= world.layers:
            return  # invalid layer, shouldn't happen if coded carefully

        # For collision, let's see if the map tile is passable
        # If it's 0 => passable, if >0 => blocked. 
        # Make sure we're not out of map bounds:
        if 0 <= int_y < len(world.map_data[self.layer]) and 0 <= int_x < len(world.map_data[self.layer][0]):
            tile_value = world.map_data[self.layer][int_y][int_x]
            if tile_value == 0:
                # It's passable => we can move
                self.grid_x = new_x
                self.grid_y = new_y
            else:
                # It's blocked => do not update grid_x or grid_y
                # You could add code to “slide” the player or handle partial collisions here
                print("Blocked by tile:", tile_value)
        else:
            # Out of map range => do nothing or handle edge collisions
            print("Out of map bounds")

    def jump(self, direction, world):
        """
        Move up or down a layer, if there's a non-zero block in that layer.
        """
        int_x = int(self.grid_x)
        int_y = int(self.grid_y)


        if direction == "up" and self.layer > 6:
            self.layer -= 1
        elif direction == "down" and self.layer < (world.layers - 1):
            self.layer += 1

        # If jumping 'up' means going to layer -1
        if direction == "up" and self.layer > 0:
            # Check the tile in the layer above
            if world.map_data[self.layer - 1][int_y][int_x] != 0:
                self.layer -= 1
            else:
                print("No block above (cannot jump up).")

        # If jumping 'down' means going to layer +1
        elif direction == "down" and self.layer < world.layers - 1:
            # Check the tile in the layer below
            if world.map_data[self.layer + 1][int_y][int_x] != 0:
                self.layer += 1
            else:
                print("No block below (cannot jump down).")


    def draw(self, surface, camera):
        """
        Draw the player in isometric coordinates. 
        The formula is the same as in the World rendering, but based on player's self.grid_x/Y.
        """
        iso_x = (self.grid_x - self.grid_y) * PLAYER_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * PLAYER_SIZE // 4 - self.layer * PLAYER_SIZE // 2

        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - PLAYER_SIZE // 2
        draw_y = iso_y + int(SCREEN_HEIGHT // 3.5) + camera.offset_y - PLAYER_SIZE // 2
    
        surface.blit(self.texture, (draw_x, draw_y))
