# modules/player.py
import pygame
<<<<<<< HEAD

from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE , PLAYER_SIZE 

class Player:
    def __init__(self, x, y, layer=1, speed=100, texture_path="assets/img/blocks/player.png"):
=======
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
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
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
        # Calculate the new position based on movement input
        new_x = self.grid_x + dx * self.speed * dt
        new_y = self.grid_y + dy * self.speed * dt
    
        # Convert to int for checking collisions on the tile grid
        int_new_x = int(new_x)
        int_new_y = int(new_y)
<<<<<<< HEAD

        # Get the topmost layer and block at the target position
        top_layer, block_id = world.get_top_layer_at(int_new_x, int_new_y)

        if top_layer is not None:
            # There is a block at this position
            if world.is_block_walkable(block_id):
                # Player can stand on this block
                self.grid_x = new_x
                self.grid_y = new_y
                self.layer = top_layer
            else:
                # Block is not walkable, so player cannot move there
                # Do not update player position
                pass
        else:
            # No block present at this position
            # If you want the player to still stand on "ground" when there's no block,
            # consider setting layer to 0 as a default ground layer.
            # Or, if you don't want the player to move into empty space, do nothing.
            
            # Example: assume layer 0 is ground even if block_id=0
            self.grid_x = new_x
            self.grid_y = new_y
            self.layer = 0

    def jump(self, direction, world):
        # Example of layer changing by jumping
=======
    
        from modules.config import SOLID_BLOCKS  # or pass it in some way
    
        if world.is_position_walkable(self.layer, int_new_x, int_new_y, SOLID_BLOCKS):
            self.grid_x = new_x
            self.grid_y = new_y
        else:
            # Collided with a solid block – do not update position
            pass

    def jump(self, direction, world):
        """Jump between layers, if within bounds."""
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
        int_x = int(self.grid_x)
        int_y = int(self.grid_y)

        if direction == "up" and self.layer > 0:
<<<<<<< HEAD
            if world.map_data[self.layer - 1][int_y][int_x] > 0:
                self.layer -= 1
            else:
                # No block above
                pass
        elif direction == "down" and self.layer < world.layers - 1:
            # Check if block below is walkable
            below_layer = self.layer + 1
            block_id = world.map_data[below_layer][int_y][int_x]
            if block_id > 0 and world.is_block_walkable(block_id):
                self.layer = below_layer

    def draw(self, surface, camera):
        # Calculate isometric position
=======
            self.layer -= 1
        elif direction == "down" and self.layer < (world.layers - 1):
            self.layer += 1

    def draw(self, surface, camera):
        """
        Convert (grid_x, grid_y) to isometric and draw the player.
        """
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE // 4 - self.layer * BLOCK_SIZE // 2

        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - BLOCK_SIZE // 2
        draw_y = iso_y + int(SCREEN_HEIGHT // 3.5) + camera.offset_y - BLOCK_SIZE // 2

        surface.blit(self.texture, (draw_x, draw_y))
<<<<<<< HEAD

    def adjust_player_layer(self, enemies):
        """Adjust the player's layer based on the position relative to enemies."""
        for enemy in enemies:
            if self.rect.y > enemy.rect.y:
                self.layer = 1  # Player is behind the enemy
            else:
                self.layer = 0  # Player is in front of the enemy


    def collides_with_blocks(self, new_x, new_y, world):
        """Check for collision with blocks in the world map."""
        # Convert new coordinates to grid coordinates (assuming tile map is used)
        grid_x = new_x // BLOCK_SIZE
        grid_y = new_y // BLOCK_SIZE
        
        # Check if the new position would collide with a non-empty block
        if world.map_data[grid_y][grid_x] == 0:  # Assuming 0 means no block
            return True
        return False
=======
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
