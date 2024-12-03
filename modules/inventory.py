# modules/world.py

import pygame
import sys
from config import BLOCK_SIZE, SCALE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from .animated_sprite import AnimatedSprite  # Changed to relative import

class World:
    def __init__(self, map_file):
        self.layers = 3  # Number of layers
        self.map_data = self.load_map_from_file(map_file)
        self.player_start_pos = self.find_player_start_position()

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
            print(f"Map file '{file_path}' not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()

    def find_player_start_position(self):
        """
        Finds the position of block '5' on the second layer to set the player's starting position.

        :return: Tuple (x, y, layer_index).
        """
        layer_index = 1  # Second layer (index 1)
        for y, row in enumerate(self.map_data[layer_index]):
            for x, block in enumerate(row):
                if block == 5:
                    return (x, y, layer_index)
        # If block '5' not found, set default position
        print("Block '5' not found on the second layer. Setting default position.")
        return (0, 0, layer_index)

    def render(self, surface, textures, camera):
        """
        Renders the map with camera offset.

        :param surface: Pygame surface to draw on.
        :param textures: Dictionary of block textures.
        :param camera: Camera object for offset.
        """
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:
                        if block == 6 and isinstance(textures["6"], AnimatedSprite):
                            # Animated block
                            iso_x = (x - y) * BLOCK_SIZE * SCALE_SIZE // 2
                            iso_y = (x + y) * BLOCK_SIZE * SCALE_SIZE // 4 - layer_index * BLOCK_SIZE * SCALE_SIZE // 2

                            # Camera offset
                            draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                            draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y

                            textures["6"].draw(surface, draw_x, draw_y)
                        else:
                            # Static block
                            texture = textures.get(str(block), None)
                            if texture:
                                iso_x = (x - y) * BLOCK_SIZE * SCALE_SIZE // 2
                                iso_y = (x + y) * BLOCK_SIZE * SCALE_SIZE // 4 - layer_index * BLOCK_SIZE * SCALE_SIZE // 2

                                # Camera offset
                                draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                                draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y

                                surface.blit(texture, (draw_x, draw_y))
