# modules/weapon.py

import pygame
from modules.resource_loader import load_image
from modules.logger import setup_logger

logger = setup_logger()

class Weapon:
    def __init__(self, name, image_path, strength=10):
        """
        Initializes a weapon.

        :param name: Name of the weapon.
        :param image_path: Path to the weapon's image.
        :param strength: Strength of the weapon determining destruction power.
        """
        self.name = name
        self.image = load_image(image_path, scale=(40, 40))
        self.strength = strength  # Percentage (e.g., 20 for 20%)

    def attack(self, direction, player, world):
        """
        Executes an attack in a given direction, affecting blocks based on weapon strength.

        :param direction: Direction of the attack ('left', 'right', 'up', 'down').
        :param player: Player object performing the attack.
        :param world: World object to interact with blocks.
        """
        # Define the number of blocks affected based on strength
        total_blocks = int((self.strength / 100) * 10)  # Example: 20% strength -> 2 blocks
        if total_blocks < 1:
            total_blocks = 1

        # Calculate block positions based on direction
        affected_blocks = []
        for i in range(1, total_blocks + 1):
            if direction == 'left':
                target_x = int(player.grid_x - i)
                target_y = int(player.grid_y)
            elif direction == 'right':
                target_x = int(player.grid_x + i)
                target_y = int(player.grid_y)
            elif direction == 'up':
                target_x = int(player.grid_x)
                target_y = int(player.grid_y - i)
            elif direction == 'down':
                target_x = int(player.grid_x)
                target_y = int(player.grid_y + i)
            else:
                logger.warning(f"Invalid attack direction: {direction}")
                continue

            # Append to affected blocks list
            affected_blocks.append((target_x, target_y))

        # Apply destruction levels
        for index, (x, y) in enumerate(affected_blocks):
            try:
                block_id = world.map_data[player.layer][y][x]
                block = world.get_block(block_id)
                if block and block.is_solid:
                    if index < 3:
                        # Fully destroy the block
                        world.map_data[player.layer][y][x] = 0
                        logger.info(f"Block '{block.name}' at ({x}, {y}) fully destroyed.")
                    elif index < 5:
                        # Half damage (this requires block state management)
                        # Example: Change block color or state
                        logger.info(f"Block '{block.name}' at ({x}, {y}) half damaged.")
                        # Implement actual half damage logic here
                    else:
                        # Quarter damage
                        logger.info(f"Block '{block.name}' at ({x}, {y}) quarter damaged.")
                        # Implement actual quarter damage logic here
            except IndexError:
                logger.error(f"Attack out of bounds at ({x}, {y})")
                continue
    def apply_damage(self, world, block, x, y, damage):
        """
        Applies damage to a block by reducing its damage level.

        :param world: World object.
        :param block: Block object.
        :param x: X-coordinate of the block.
        :param y: Y-coordinate of the block.
        :param damage: Amount of damage to apply (0.25, 0.5, etc.).
        """
        current_damage = getattr(block, 'damage_level', 0)
        new_damage = current_damage + damage

        if new_damage >= 1:
            # Fully destroy the block
            world.map_data[block.layer][y][x] = 0
            logger.info(f"Block '{block.name}' at ({x}, {y}) fully destroyed after damage.")
        else:
            # Update block's damage level
            block.damage_level = new_damage
            logger.info(f"Block '{block.name}' at ({x}, {y}) damage level updated to {block.damage_level}.")