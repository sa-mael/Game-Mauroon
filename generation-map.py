import random

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
MAP_WIDTH = 142
MAP_HEIGHT = 142

# We’ll generate these layers as an example:
#   Layer 0: Very hard rock (1)
#   Layer 1: Very hard rock (1)
#   Layer 2: Hard rock (2)
#   Layer 3: Possibly water / grass / etc.
#   ...
#   We'll go up to, say, Layer 7 or 8 as you requested.
TOTAL_LAYERS = 9  # You can go higher if needed

# Helper: Turn a 2D list of ints into lines like "1.1.1.2.2.1"
def format_layer(layer_data):
    lines = []
    for row in layer_data:
        line_str = ".".join(str(val) for val in row)
        lines.append(line_str)
    return "\n".join(lines)

def generate_layer(layer_index):
    """
    Return a 2D list (MAP_HEIGHT x MAP_WIDTH) 
    for the given layer_index, using your ID scheme.
    """
    # Create a default fill
    # e.g. fill everything with 1 (very hard rock) for lower layers
    layer_map = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    
    # Example logic:
    if layer_index == 0 or layer_index == 1:
        # Fill everything with "1" = very hard rock
        pass
    
    elif layer_index == 2:
        # Fill everything with "2" = hard rock
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                layer_map[y][x] = 2
    
    elif layer_index == 3:
        # Let’s say we fill with "3" = regular rock
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                layer_map[y][x] = 3
    
    elif layer_index == 4:
        # Fill with "4" = dirt
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                layer_map[y][x] = 4
    
    elif layer_index == 5:
        # Example water layer: "5" = water
        # We can create a random "river" or "lake" area
        # For demonstration, let's randomly fill part of the layer with water.
        # But you’ll adapt it to your real river/lake logic.
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # 1/5 chance to be water, else 0
                # (In your real code you might carve a path for the river or lake).
                rand_val = random.random()
                if rand_val < 0.2:
                    layer_map[y][x] = 5
                else:
                    layer_map[y][x] = 0  # 0 means "no block"
    
    elif layer_index == 6:
        # "6" = grass
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                layer_map[y][x] = 6
    
    elif layer_index == 7:
        # Mix ramps (12, 13) and some special block IDs (14-17).
        # Let’s do a simple pattern in the top-left corner as a demo.
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # We'll fill with "6" = grass by default
                layer_map[y][x] = 6
                
        # Add a diagonal line of ramps
        for i in range(min(MAP_WIDTH, MAP_HEIGHT)):
            if i % 2 == 0:
                layer_map[i][i] = 12  # up-down ramp
            else:
                layer_map[i][i] = 13  # left-right ramp
        
        # Add a small 4x4 block of "energy field" in top-left
        for y2 in range(4):
            for x2 in range(4):
                # We'll vary 14,15,16,17 just for demonstration
                layer_map[y2][x2] = random.choice([14, 15, 16, 17])
    
    elif layer_index == 8:
        # Suppose layer 8 is for "torch (18)" or "tent (19)".
        # We'll randomly place them:
        layer_map = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        # Place random torches
        for _ in range(20):
            rx = random.randint(0, MAP_WIDTH - 1)
            ry = random.randint(0, MAP_HEIGHT - 1)
            layer_map[ry][rx] = 18  # torch
        
        # Place random tents
        for _ in range(5):
            rx = random.randint(0, MAP_WIDTH - 1)
            ry = random.randint(0, MAP_HEIGHT - 1)
            layer_map[ry][rx] = 19  # tent
    
    return layer_map

def generate_map_txt(filename="map.txt"):
    """
    Generates a multi-layer map file with the format:
      # Layer 0
      1.1.1.1...
      1.1.1.1...
      ...
      # Layer 1
      ...
    """
    with open(filename, "w") as f:
        for layer_idx in range(TOTAL_LAYERS):
            # Write the layer header
            f.write(f"# Layer {layer_idx}\n")
            data_2d = generate_layer(layer_idx)
            # Convert 2D list to lines "X.X.X.X"
            layer_str = format_layer(data_2d)
            f.write(layer_str + "\n")

if __name__ == "__main__":
    generate_map_txt("generated_map.txt")
    print("Map generated: 'generated_map.txt'")
