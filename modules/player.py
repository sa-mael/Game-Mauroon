import sys
import pygame
from .config import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SIZE

class Player:
    def __init__(self, x, y, layer=1, speed=10, texture_path="assets/img/blocks/player.png"):
        self.grid_x = x
        self.grid_y = y
        self.layer = layer
        self.speed = speed

        # Load player texture
        try:
            self.texture = pygame.image.load(texture_path).convert_alpha()
            self.texture = pygame.transform.scale(self.texture, (PLAYER_SIZE, PLAYER_SIZE))
        except pygame.error as e:
            print(f"Error loading player texture '{texture_path}': {e}")
            sys.exit()

    def direction(self, direction):
        if direction == "up":
            self.texture = pygame.image.load("assets/img/blocks/player_back.png").convert_alpha()
        elif direction == "down":
            self.texture = pygame.image.load("assets/img/blocks/player_front.png").convert_alpha()
        elif direction == "left":
            self.texture = pygame.image.load("assets/img/blocks/player_left.png").convert_alpha()
        elif direction == "right":
            self.texture = pygame.image.load("assets/img/blocks/player_right.png").convert_alpha()
        else:
            self.texture = pygame.image.load("assets/img/blocks/player.png").convert_alpha()
    def move(self, dx, dy, dt, world):
        new_x = self.grid_x + (dx + dy) * self.speed * dt / 2**0.5
        new_y = self.grid_y + (dy - dx) * self.speed * dt / 2**0.5

        int_new_x = int(new_x)
        int_new_y = int(new_y)

        if (0 <= int_new_x < len(world.map_data[self.layer][0]) and
            0 <= int_new_y < len(world.map_data[self.layer]) and
            world.map_data[self.layer][int_new_y][int_new_x] > 0 and
            world.map_data[self.layer + 1][int_new_y][int_new_x] == 0):
            self.grid_x, self.grid_y = new_x, new_y
        else:
            # Position blocked
            pass

    def jump(self, direction, world):
        int_x = int(self.grid_x)
        int_y = int(self.grid_y)

        if direction == "up" and self.layer > 0:
            if world.map_data[self.layer - 1][int_y][int_x] > 0:
                self.layer -= 1
            else:
                # No block above
                pass
        elif direction == "down" and self.layer < world.layers - 1:
            if world.map_data[self.layer + 1][int_y][int_x] > 0:
                self.layer += 1
            else:
                # No block below
                pass

    def draw(self, surface, camera):
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE // 4 - self.layer * BLOCK_SIZE // 2

        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - PLAYER_SIZE // 2
        draw_y = iso_y + int(SCREEN_HEIGHT // 3.5) + camera.offset_y - PLAYER_SIZE // 2

        surface.blit(self.texture, (draw_x, draw_y))
    
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