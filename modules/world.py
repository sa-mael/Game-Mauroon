import sys
from .config import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class World:
    def __init__(self, map_file):
        self.layers = 5
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
                    chunks[current_layer].append([int(char) for char in line])
            return chunks
        except FileNotFoundError:
            print(f"Map file '{file_path}' not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()

    def find_player_start_position(self):
        layer_index = 1
        for y, row in enumerate(self.map_data[layer_index]):
            for x, block in enumerate(row):
                if block == 5:
                    return (x, y, layer_index)
        print("Block '5' not found on layer 1. Setting default player position.")
        return (0, 0, layer_index)

    def render(self, surface, textures, camera):
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:
                        # Isometric conversion
                        iso_x = (x - y) * BLOCK_SIZE // 2
                        iso_y = (x + y) * BLOCK_SIZE // 4 - layer_index * BLOCK_SIZE // 2

                        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                        draw_y = iso_y + int(SCREEN_HEIGHT // 3.5) + camera.offset_y

                        if str(block) in textures and textures[str(block)] is not None:
                            # Could be animated or static
                            tex = textures[str(block)]
                            if hasattr(tex, 'draw'):
                                tex.draw(surface, draw_x, draw_y)
                            else:
                                surface.blit(tex, (draw_x, draw_y))
