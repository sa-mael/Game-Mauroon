# modules/world.py

import pygame
import sys
from config import BLOCK_SIZE, SCALE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from modules.animated_sprite import AnimatedSprite
from modules.resource_loader import load_image
from modules.logger import setup_logger

logger = setup_logger()

class World:
    def __init__(self, map_file):
        self.layers = 3  # Number of layers
        self.map_data = self.load_map_from_file(map_file)
        self.player_start_pos = self.find_player_start_position()
        self.blocks = self.load_blocks()

    def load_map_from_file(self, file_path):
        """
        Loads the map from a text file, separating it into layers.

        :param file_path: Path to the map file.
        :return: List of map layers.
        """
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            chunks = []
            current_layer = -1

            for line in lines:
                line = line.strip()
                if line.startswith("# Layer"):
                    current_layer += 1
                    chunks.append([])
                    continue
                if line and current_layer >= 0:
                    chunks[current_layer].append([int(char) for char in line])
            return chunks

        except FileNotFoundError:
            logger.error(f"Map file '{file_path}' not found!")
            sys.exit()
        except Exception as e:
            logger.error(f"Error loading map: {e}")
            sys.exit()

    def find_player_start_position(self):
        """
        Finds the position of block '5' on the second layer to set the player's starting position.

        :return: Tuple (x, y, layer_index).
        """
        layer_index = 1  # Second layer (index 1)
        try:
            for y, row in enumerate(self.map_data[layer_index]):
                for x, block in enumerate(row):
                    if block == 5:
                        return (x, y, layer_index)
            # If block '5' not found, set default position
            logger.warning("Block '5' not found on the second layer. Setting default position.")
            return (0, 0, layer_index)
        except IndexError as e:
            logger.error(f"Error finding player start position: {e}")
            sys.exit()

    def load_blocks(self):
        """
        Loads block definitions from a JSON file or defines them manually.

        :return: Dictionary mapping block IDs to Block objects.
        """
        # Example: Define blocks manually or load from a JSON file
        blocks = {
            1: Block(
                block_id=1,
                name="Stone",
                image_path="assets/img/blocks/stone.png",
                is_solid=True,
                mining_level=1
            ),
            2: Block(
                block_id=2,
                name="Grass",
                image_path="assets/img/blocks/grass.png",
                is_solid=True,
                mining_level=1
            ),
            3: Block(
                block_id=3,
                name="Tree",
                image_path="assets/img/blocks/tree.png",
                is_solid=True,
                mining_level=2
            ),
            4: Block(
                block_id=4,
                name="Grass1",
                image_path="assets/img/blocks/grass1.png",
                is_solid=True,
                mining_level=1
            ),
            5: Block(
                block_id=5,
                name="PlayerStart",
                image_path="assets/img/blocks/block_5.png",
                is_solid=False,
                mining_level=0
            ),
            6: Block(
                block_id=6,
                name="AnimatedBlock",
                image_path="assets/img/blocks/ARW2DSprite.png",
                is_solid=True,
                mining_level=1,
                animated=True
            )
            # Add more blocks as needed
        }
        return blocks

    def get_block(self, block_id):
        """
        Retrieves a Block object based on its ID.

        :param block_id: The ID of the block.
        :return: Block object or None if not found.
        """
        return self.blocks.get(block_id, None)

    def render(self, surface, textures, camera):
        """
        Renders the map with camera offset.

        :param surface: Pygame surface to draw on.
        :param textures: Dictionary of block textures.
        :param camera: Camera object for offset.
        """
         for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block_id in enumerate(row):
                    if block_id > 0:
                        block = self.get_block(block_id)
                        if block:
                            iso_x = (x - y) * BLOCK_SIZE * SCALE_SIZE // 2
                            iso_y = (x + y) * BLOCK_SIZE * SCALE_SIZE // 4 - layer_index * BLOCK_SIZE * SCALE_SIZE // 2

                            # Camera offset
                            draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                            draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y

                            # Check block damage
                            damage_level = getattr(block, 'damage_level', 0)

                            if block.animated:
                                animated_sprite = textures.get(str(block_id), None)
                                if isinstance(animated_sprite, AnimatedSprite):
                                    animated_sprite.draw(surface, draw_x, draw_y)
                                    animated_sprite.update(1 / FPS)  # Update animation based on frame rate
                            else:
                                block_image = block.get_image(damage_level)
                                if block_image:
                                    try:
                                        surface.blit(block_image, (draw_x, draw_y))
                                    except Exception as e:
                                        logger.error(f"Error rendering block '{block.name}' at ({x}, {y}): {e}")
                                else:
                                    # Block is fully destroyed
                                    pass
                        else:
                            logger.warning(f"Undefined block ID '{block_id}' at ({x}, {y}, Layer {layer_index})")