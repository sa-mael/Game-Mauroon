# modules/player.py

import pygame
import sys
from config import BLOCK_SIZE, SCALE_SIZE, PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y, layer=1, speed=5, texture_path="assets/img/blocks/player.png"):
        self.grid_x = x
        self.grid_y = y
        self.layer = layer  # Player's current layer
        self.speed = speed  # Movement speed

        # Load player texture
        try:
            self.texture = pygame.image.load(texture_path).convert_alpha()
            self.texture = pygame.transform.scale(self.texture, (PLAYER_SIZE, PLAYER_SIZE))
        except pygame.error as e:
            print(f"Error loading player texture '{texture_path}': {e}")
            sys.exit()

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
        if (
            0 <= int_new_x < len(world.map_data[self.layer][0]) and
            0 <= int_new_y < len(world.map_data[self.layer]) and
            world.map_data[self.layer][int_new_y][int_new_x] > 0
        ):
            self.grid_x, self.grid_y = new_x, new_y
        else:
            print("Cannot move to that position.")

    def jump(self, direction, world):
        """
        Allows the player to jump up or down between layers.

        :param direction: "up" to jump up, "down" to go down.
        :param world: World object to check for possible jumps.
        """
        int_x = int(self.grid_x)
        int_y = int(self.grid_y)

        if direction == "up" and self.layer > 0:
            # Attempt to jump up
            if world.map_data[self.layer - 1][int_y][int_x] > 0:
                self.layer -= 1
            else:
                print("Cannot jump up; no block above.")
        elif direction == "down" and self.layer < world.layers - 1:
            # Attempt to jump down
            if world.map_data[self.layer + 1][int_y][int_x] > 0:
                self.layer += 1
            else:
                print("Cannot jump down; no block below.")
        else:
            print("Cannot perform jump.")

    def mine_block(self, world, inventory, crafting):
        """
        Attempts to mine the block the player is facing using the appropriate tool.

        :param world: World object to interact with the map.
        :param inventory: Player's Inventory object.
        :param crafting: Crafting system for adding mined items.
        """
        # Determine the block the player is facing (e.g., in front)
        target_x = int(self.grid_x + 1)  # Example: block to the right
        target_y = int(self.grid_y)

        # Check if the target block is within map boundaries
        if (
            0 <= target_x < len(world.map_data[self.layer][0]) and
            0 <= target_y < len(world.map_data[self.layer]) and
            world.map_data[self.layer][target_y][target_x] > 0
        ):
            block_id = world.map_data[self.layer][target_y][target_x]
            block = world.get_block(block_id)

            # Check if the player has the required tool
            if block.mining_level <= inventory.get_tool_level():
                # Remove the block from the world
                world.map_data[self.layer][target_y][target_x] = 0

                # Add the block as an item to the inventory
                mined_item = Item(name=block.name, image_path=block.image_path, quantity=1)
                inventory.add_item(mined_item)
                print(f"Mined '{block.name}'.")
            else:
                print(f"Need a better tool to mine '{block.name}'.")
        else:
            print("No block to mine in that direction.")

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

        surface.blit(self.texture, (draw_x, draw_y))
