import random

# Constants
MAP_WIDTH = 142
MAP_HEIGHT = 142
LAYERS = 9  # 0-8 layers

# Initialize map layers
map_layers = [[[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)] for _ in range(LAYERS)]

# Helper Functions
def fill_layer(layer_index, value):
    """Fill an entire layer with a single value."""
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            map_layers[layer_index][y][x] = value

def generate_river():
    """Generate a vertically aligned river."""
    river_x = random.randint(MAP_WIDTH // 4, MAP_WIDTH * 3 // 4)  # River starting x-coordinate
    river_width = 1  # Start with 1 block wide at the base

    for z in range(3, 8):  # Layers 3 to 7
        for y in range(MAP_HEIGHT):
            for offset in range(-river_width // 2, river_width // 2 + 1):
                if 0 <= river_x + offset < MAP_WIDTH:
                    map_layers[z][y][river_x + offset] = 5  # Water
            # Meander slightly
            river_x += random.choice([-1, 0, 1])
            river_x = max(0, min(MAP_WIDTH - 1, river_x))  # Keep within bounds
        # Increase width as we move up
        river_width = min(river_width + 1, 5)

def generate_lakes():
    """Generate lakes."""
    for _ in range(4):  # Number of lakes
        center_x = random.randint(20, MAP_WIDTH - 20)
        center_y = random.randint(20, MAP_HEIGHT - 20)
        lake_size = random.randint(9, 21)

        for _ in range(lake_size):
            lx = center_x + random.randint(-4, 4)
            ly = center_y + random.randint(-4, 4)
            if 0 <= lx < MAP_WIDTH and 0 <= ly < MAP_HEIGHT:
                for z in range(5, 8):  # Lakes span layers 5–7
                    map_layers[z][ly][lx] = 5

def generate_forest():
    """Generate forests."""
    for _ in range(8):  # Number of forests
        center_x = random.randint(10, MAP_WIDTH - 10)
        center_y = random.randint(10, MAP_HEIGHT - 10)
        tree_count = random.randint(5, 43)

        for _ in range(tree_count):
            tx = center_x + random.randint(-3, 3)
            ty = center_y + random.randint(-3, 3)
            if 0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT:
                map_layers[7][ty][tx] = random.choice([8, 9])  # Dark or Light Wood

def generate_paths():
    """Generate 2-block-wide paths."""
    for _ in range(6):  # Number of paths
        x, y = random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)
        for _ in range(50):  # Path length
            map_layers[7][y][x] = 12  # Path (Ramp up-down)
            for offset in range(2):  # Make path 2 blocks wide
                if 0 <= x + offset < MAP_WIDTH:
                    map_layers[7][y][x + offset] = 12
            x += random.choice([-1, 1])
            y += random.choice([-1, 1])
            x, y = max(0, min(MAP_WIDTH - 1, x)), max(0, min(MAP_HEIGHT - 1, y))

def generate_energy_fields():
    """Generate energy fields."""
    quadrants = [
        (14, 0, MAP_WIDTH // 2, 0, MAP_HEIGHT // 2),  # Upper-left
        (15, MAP_WIDTH // 2, MAP_WIDTH, 0, MAP_HEIGHT // 2),  # Upper-right
        (16, 0, MAP_WIDTH // 2, MAP_HEIGHT // 2, MAP_HEIGHT),  # Lower-left
        (17, MAP_WIDTH // 2, MAP_WIDTH, MAP_HEIGHT // 2, MAP_HEIGHT),  # Lower-right
    ]
    for value, x1, x2, y1, y2 in quadrants:
        for _ in range(15):  # Points per quadrant
            x, y = random.randint(x1, x2 - 1), random.randint(y1, y2 - 1)
            map_layers[7][y][x] = value

def add_surface_objects():
    """Add torches and tents to layer 8."""
    for _ in range(10):  # Add torches
        x, y = random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)
        map_layers[8][y][x] = 8  # Torch

    for _ in range(5):  # Add tents
        x, y = random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)
        map_layers[8][y][x] = 9  # Tent

# Generate Terrain
fill_layer(0, 1)  # Very Hard Rock
fill_layer(1, 1)
fill_layer(2, 1)
fill_layer(3, 2)  # Hard Rock
fill_layer(4, 2)
fill_layer(5, 3)  # Regular Rock
fill_layer(6, 4)  # Dirt

generate_river()
generate_lakes()
generate_forest()
generate_paths()
generate_energy_fields()
add_surface_objects()

# Save Map to File
with open("generated_map.txt", "w") as f:
    for z, layer in enumerate(map_layers):
        f.write(f"# Layer {z}\n")
        for row in layer:
            f.write(".".join(map(str, row)) + "\n")
        f.write("\n")
