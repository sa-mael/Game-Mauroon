<<<<<<< HEAD
# world.py
# This module defines the World class and handles map loading, rendering, and block lookups.

import sys
import pygame
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE
from .block import is_block_walkable
from .animated_sprite import AnimatedSprite

class World:
    def __init__(self, map_file):
        self.layers = 3
=======
# modules/world.py
import sys
import pygame
from modules.config import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from modules.animated_sprite import AnimatedSprite

class World:
    def __init__(self, map_file):
        """
        Loads the map from a file containing multiple layers.
        For example:
            # Layer 0
            1111
            1001
            ...
            # Layer 1
            ...
            # Layer 2
            ...
        """
        self.layers = 5  # or however many layers your map.txt has
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
        self.map_data = self.load_map_from_file(map_file)
        self.layers = len(self.map_data)
        self.player_start_pos = self.find_player_start_position()
        self.textures = textures

    def load_map_from_file(self, file_path):
        """
        Load map from a text file. Expected format:
        # Layer 0
        1 1 23 53 33 53
        1 23 23 23 23 23
        # Layer 1
        1 1 1 1 1 1
        ...
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
<<<<<<< HEAD
                    # Split line by spaces and convert to int
                    row = [int(x) for x in line.split()]
                    chunks[current_layer].append(row)
=======
                    row_data = [int(char) for char in line]
                    chunks[current_layer].append(row_data)

>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
            return chunks

        except FileNotFoundError:
            print(f"Map file '{file_path}' not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()

    def find_player_start_position(self):
        """
<<<<<<< HEAD
        Find the position of a special block (e.g., block type 5)
        as the player's start position. If not found, return (0,0,1).
=======
        Look for '5' in layer 1 as the player's start.
        If not found, default to (0, 0, layer 1).
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
        """
        layer_index = 1
        if layer_index < len(self.map_data):
            for y, row in enumerate(self.map_data[layer_index]):
                for x, block in enumerate(row):
                    if block == 5:
                        return (x, y, layer_index)
        return (0, 0, layer_index)

<<<<<<< HEAD
    def render(self, surface, camera):
        """
        Render the world layers in isometric view.
        """
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block_type in enumerate(row):
                    if block_type > 0:
=======
    def render(self, surface, textures, camera):
        """
        Draw each layer in isometric projection.
        """
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:
                        block_key = str(block)
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
                        iso_x = (x - y) * BLOCK_SIZE // 2
                        iso_y = (x + y) * BLOCK_SIZE // 4 - layer_index * BLOCK_SIZE // 2

                        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                        draw_y = iso_y + int(SCREEN_HEIGHT // 3.5) + camera.offset_y

<<<<<<< HEAD
                        block_tex = self.textures.get(str(block_type), None)
                        if block_tex is not None:
                            # If the texture is an AnimatedSprite, it has a draw method
                            if hasattr(block_tex, "draw"):
                                block_tex.draw(surface, draw_x, draw_y)
                            else:
                                surface.blit(block_tex, (draw_x, draw_y))

    def is_walkable(self, layer, grid_x, grid_y):
        """
        Check if the block at given coordinates is walkable.
        """
        if 0 <= grid_y < len(self.map_data[layer]) and 0 <= grid_x < len(self.map_data[layer][0]):
            block_type = self.map_data[layer][grid_y][grid_x]
            return is_block_walkable(block_type)
        return False
=======
                        if block_key in textures and isinstance(textures[block_key], AnimatedSprite):
                            # Animated block
                            textures[block_key].draw(surface, draw_x, draw_y)
                        elif block_key in textures and textures[block_key] is not None:
                            # Static texture
                            surface.blit(textures[block_key], (draw_x, draw_y))
                        else:
                            # No valid texture (block > 0 but no image loaded)
                            pass
    def is_position_walkable(self, layer, x, y, solid_blocks_set):
        # Check layer boundaries
        if layer < 0 or layer >= len(self.map_data):
            return False
        # Check row/column boundaries
        if y < 0 or y >= len(self.map_data[layer]):
            return False
        if x < 0 or x >= len(self.map_data[layer][y]):
            return False
    
        block_id = self.map_data[layer][y][x]
        return block_id not in solid_blocks_set
>>>>>>> 0a5bd4cfb6dab00b8c259011c834fbdd314170fb
