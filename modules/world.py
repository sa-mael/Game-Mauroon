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
        self.layers = 3  # or however many layers your map.txt has
        self.map_data = self.load_map_from_file(map_file)
        self.player_start_pos = self.find_player_start_position()

    def load_map_from_file(self, file_path):
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
                    row_data = [int(char) for char in line]
                    chunks[current_layer].append(row_data)

            return chunks

        except FileNotFoundError:
            print(f"Map file '{file_path}' not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()

    def find_player_start_position(self):
        """
        Look for '5' in layer 1 as the player's start.
        If not found, default to (0, 0, layer 1).
        """
        layer_index = 1
        if layer_index < len(self.map_data):
            for y, row in enumerate(self.map_data[layer_index]):
                for x, block in enumerate(row):
                    if block == 5:
                        return (x, y, layer_index)
        return (0, 0, layer_index)

    def render(self, surface, textures, camera):
        """
        Draw each layer in isometric projection.
        """
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:
                        block_key = str(block)
                        iso_x = (x - y) * BLOCK_SIZE // 2
                        iso_y = (x + y) * BLOCK_SIZE // 4 - layer_index * BLOCK_SIZE // 2

                        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                        draw_y = iso_y + int(SCREEN_HEIGHT // 3.5) + camera.offset_y

                        if block_key in textures and isinstance(textures[block_key], AnimatedSprite):
                            # Animated block
                            textures[block_key].draw(surface, draw_x, draw_y)
                        elif block_key in textures and textures[block_key] is not None:
                            # Static texture
                            surface.blit(textures[block_key], (draw_x, draw_y))
                        else:
                            # No valid texture (block > 0 but no image loaded)
                            pass
