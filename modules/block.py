# modules/block.py

import pygame
import sys
from modules.resource_loader import load_image
from modules.logger import setup_logger

logger = setup_logger()

class Block:
    def __init__(self, block_id, name, image_path, is_solid=True, mining_level=1, animated=False, layer=0):
        """
        Initializes a block type.

        :param block_id: Unique identifier for the block.
        :param name: Name of the block.
        :param image_path: Path to the block's image.
        :param is_solid: Whether the block is solid (player cannot pass through).
        :param mining_level: The level required to mine the block.
        :param animated: Whether the block has an animated sprite.
        :param layer: The layer the block belongs to.
        """
        self.block_id = block_id
        self.name = name
        self.is_solid = is_solid
        self.mining_level = mining_level
        self.animated = animated
        self.layer = layer
        self.image_path = image_path

        # Load block images for different damage levels
        self.image_full = load_image(image_path, scale=(40, 40))[0]
        self.image_half = self.create_half_damage_image()
        self.image_quarter = self.create_quarter_damage_image()
        self.damage_level = 0  # 0: No damage, 0.25: Quarter, 0.5: Half, 0.75: Three Quarters, 1: Fully Destroyed

    def create_half_damage_image(self):
        """Creates a half-damaged version of the block image."""
        try:
            half_image = self.image_full.copy()
            pygame.draw.rect(half_image, (255, 0, 0), half_image.get_rect(), width=5)  # Example: Red outline
            return half_image
        except Exception as e:
            logger.error(f"Error creating half-damaged image for '{self.name}': {e}")
            return self.image_full

    def create_quarter_damage_image(self):
        """Creates a quarter-damaged version of the block image."""
        try:
            quarter_image = self.image_full.copy()
            pygame.draw.rect(quarter_image, (255, 255, 0), quarter_image.get_rect(), width=3)  # Example: Yellow outline
            return quarter_image
        except Exception as e:
            logger.error(f"Error creating quarter-damaged image for '{self.name}': {e}")
            return self.image_full

    def get_image(self):
        """
        Retrieves the appropriate image based on damage level.

        :return: Pygame.Surface object or None if fully destroyed.
        """
        if self.damage_level >= 1:
            return None  # Fully destroyed
        elif self.damage_level >= 0.5:
            return self.image_half
        elif self.damage_level > 0:
            return self.image_quarter
        else:
            return self.image_full

    def apply_damage(self, damage):
        """
        Applies damage to the block, updating its damage level.

        :param damage: Amount of damage to apply.
        """
        self.damage_level += damage
        if self.damage_level >= 1:
            self.damage_level = 1
            logger.info(f"Block '{self.name}' fully destroyed.")
        else:
            logger.info(f"Block '{self.name}' damage level updated to {self.damage_level}.")
