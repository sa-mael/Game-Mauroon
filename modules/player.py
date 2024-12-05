# modules/player.py

import pygame
import sys
from config import BLOCK_SIZE, SCALE_SIZE, PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from modules.resource_loader import load_image
from modules.weapon import Weapon
from modules.logger import setup_logger

logger = setup_logger()

class Player:
    def __init__(self, x, y, layer=1, speed=5, texture_path="assets/img/player.png"):
        self.grid_x = x
        self.grid_y = y
        self.layer = layer  # Player's current layer
        self.speed = speed  # Movement speed

        # Load player texture with error handling
        self.texture = load_image(texture_path, scale=(PLAYER_SIZE, PLAYER_SIZE))

        if self.texture_error:
            self.display_error = True
        else:
            self.display_error = False

        # Initialize weapons (for simplicity, one weapon)
        self.current_weapon = Weapon(name="Basic Sword", image_path="assets/img/items/sword.png", strength=20)

    # [Other methods remain unchanged]

    def move(self, dx, dy, dt, world):
        """
        Moves the player if possible.

        :param dx: Change in X.
        :param dy: Change in Y.
        :param dt: Delta time (seconds).
        :param world: World object for collision checking.
        """
        new_x = self.grid_x + dx * self.speed * dt
        new_y = self.grid_y + dy * self.speed * dt

        # Convert to integer coordinates for map indexing
        int_new_x = int(new_x)
        int_new_y = int(new_y)

        # Check map boundaries and if there's a block on the current layer
        try:
            if (
                0 <= int_new_x < len(world.map_data[self.layer][0]) and
                0 <= int_new_y < len(world.map_data[self.layer]) and
                world.map_data[self.layer][int_new_y][int_new_x] > 0
            ):
                self.grid_x, self.grid_y = new_x, new_y
            else:
                logger.warning("Cannot move to that position.")
        except IndexError as e:
            logger.error(f"Movement Error: {e}")

    def jump(self, direction, world):
        """
        Allows the player to jump up or down between layers.

        :param direction: "up" to jump up, "down" to go down.
        :param world: World object to check for possible jumps.
        """
        int_x = int(self.grid_x)
        int_y = int(self.grid_y)

        try:
            if direction == "up" and self.layer > 0:
                # Attempt to jump up
                if world.map_data[self.layer - 1][int_y][int_x] > 0:
                    self.layer -= 1
                else:
                    logger.warning("Cannot jump up; no block above.")
            elif direction == "down" and self.layer < world.layers - 1:
                # Attempt to jump down
                if world.map_data[self.layer + 1][int_y][int_x] > 0:
                    self.layer += 1
                else:
                    logger.warning("Cannot jump down; no block below.")
            else:
                logger.warning("Cannot perform jump.")
        except IndexError as e:
            logger.error(f"Jumping Error: {e}")
    
    def attack(self, direction, world):
        """
        Executes an attack in a given direction using the current weapon.

        :param direction: Direction of the attack ('left', 'right', 'up', 'down').
        :param world: World object to interact with blocks.
        """
        self.current_weapon.attack(direction, self, world)

    def draw(self, surface, camera):
        """
        Draws the player on the screen with camera offset.

        :param surface: Pygame surface to draw on.
        :param camera: Camera object for offset.
        """
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE * SCALE_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE * SCALE_SIZE // 4 - self.layer * BLOCK_SIZE * SCALE_SIZE // 2

        # Camera offset
        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - PLAYER_SIZE // 2
        draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y - PLAYER_SIZE // 2

        try:
            surface.blit(self.texture, (draw_x, draw_y))
        except Exception as e:
            logger.error(f"Drawing Player Error: {e}")
        
         surface.blit(self.texture, (draw_x, draw_y))

        if self.display_error and self.texture_error:
            # Render the error message on the screen
            error_text = font.render(self.texture_error, True, (255, 0, 0))
            surface.blit(error_text, (10, SCREEN_HEIGHT - 30))
