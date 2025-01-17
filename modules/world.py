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
        self.layers = 8 # or however many layers your map.txt has
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
                if line.startswith("# Layer"):  # Detects layer changes
                    current_layer += 1
                    chunks.append([])  # Start new layer
                    continue
                if line and current_layer >= 0:
                    try:
                        row_data = [int(x) for x in line.split('.') if x.isdigit()]  # Parse numbers, ignore separators
                        chunks[current_layer].append(row_data)
                    except ValueError:
                        print(f"Error parsing line: {line}")
                        sys.exit()
    
            return chunks
    
        except FileNotFoundError:
            print(f"Map file '{file_path}' not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()


    def find_player_start_position(self):
         """
           Look for '5' in any layer as the player's start.
            If not found, default to (0, 0, layer 1).
         """
         for layer_index, layer in enumerate(self.map_data):
             for y, row in enumerate(layer):
                 for x, block in enumerate(row):
                     if block == 14:  # Found player start
                         return (x, y, layer_index)
         return (0, 0, 1)  # Default spawn


    def render(self, surface, textures, camera):
        """
        Draw each layer in an isometric perspective.
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
      
                        if block_key in textures:
                            if isinstance(textures[block_key], AnimatedSprite):
                                textures[block_key].draw(surface, draw_x, draw_y)
                            elif textures[block_key] is not None:
                                surface.blit(textures[block_key], (draw_x, draw_y))
      
    def is_position_walkable(self, layer, x, y, solid_blocks_set):
         """
         Checks if a position is walkable by ensuring it is within bounds
         and does not contain a solid block.
         """
         # Ensure position is within world bounds
         if not (0 <= layer < len(self.map_data) and
                 0 <= y < len(self.map_data[layer]) and
                 0 <= x < len(self.map_data[layer][y])):
             return False
     
         block_id = self.map_data[layer][y][x]
         
         # Ensure that the block is not a solid one
         return block_id not in solid_blocks_set
     