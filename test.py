import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 840
BLOCK_SIZE = 22
PLAYER_SIZE = 22
SCALE_SIZE = 2
BACKGROUND_COLOR = (50, 50, 50)

# --- Initialize pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric World")
clock = pygame.time.Clock()

# --- Load Textures ---
def load_texture(path, width, height, scale_size):
    """Load and scale a texture."""
    try:
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, (width * scale_size, height * scale_size))
    except pygame.error as e:
        print(f"Error loading texture {path}: {e}")
        sys.exit()

# Load textures into a dictionary
TEXTURES = {
    "1": load_texture("img/stone.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Bottom layer
    "2": load_texture("img/grass.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Middle layer
    "3": load_texture("img/tree.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),   # Top layer
    "empty": None,
}

PLAYER_TEXTURE = load_texture("img/player.png", PLAYER_SIZE, PLAYER_SIZE, SCALE_SIZE)

# --- World Map Setup ---
class World:
    def __init__(self):
        self.layers = 3  # Number of layers (bottom, middle, top)
        self.map_data = self.load_map_from_file("maps/map.txt")  # Load map from file

    def load_map_from_file(self, file_path):
        """Load map from a text file with layers."""
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            chunks = [[] for _ in range(self.layers)]  # Create an array for layers
            current_layer = -1  # Current layer

            for line in lines:
                line = line.strip()
                if line.startswith("# Layer"):  # Switch to a new layer
                    current_layer += 1
                    continue
                if line and current_layer >= 0:
                    # Add map row to the current layer
                    chunks[current_layer].append([int(char) for char in line])

            return chunks

        except FileNotFoundError:
            print(f"Map file {file_path} not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()

    def render(self):
        """Render the map layers in isometric view."""
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:  # Skip empty blocks
                        texture = TEXTURES.get(str(block), None)
                        if texture:
                            iso_x = (x - y) * BLOCK_SIZE * SCALE_SIZE // 2
                            iso_y = (x + y) * BLOCK_SIZE * SCALE_SIZE // 4 - layer_index * BLOCK_SIZE * SCALE_SIZE // 2
                            screen.blit(texture, (iso_x + SCREEN_WIDTH // 2, iso_y + SCREEN_HEIGHT // 3.5))

# --- Player Setup ---
class Player:
    def __init__(self, x, y, layer=1, speed=1):
        self.grid_x = x
        self.grid_y = y
        self.layer = layer  # Player's current layer
        self.speed = speed

    def move(self, direction, world):
        """Move the player in a direction if possible."""
        new_x, new_y = self.grid_x, self.grid_y
        if direction == "up":
            new_y -= self.speed
        elif direction == "down":
            new_y += self.speed
        elif direction == "left":
            new_x -= self.speed
        elif direction == "right":
            new_x += self.speed

        # Check map boundaries and if there's a block on the current layer
        if (
            0 <= new_x < len(world.map_data[self.layer][0]) and  # Check X boundaries
            0 <= new_y < len(world.map_data[self.layer]) and      # Check Y boundaries
            world.map_data[self.layer][new_y][new_x] > 0          # Check for a block on the current layer
        ):
            self.grid_x, self.grid_y = new_x, new_y
        else:
            print("Cannot move to that position.")

    def jump(self, direction, world):
        """Move up or down layers if possible."""
        if direction == "up" and self.layer > 0:
            # Attempt to move up a layer
            if world.map_data[self.layer - 1][self.grid_y][self.grid_x] > 0:
                self.layer -= 1
            else:
                print("Cannot jump up; no block above.")
        elif direction == "down" and self.layer < world.layers - 1:
            # Attempt to move down a layer
            if world.map_data[self.layer + 1][self.grid_y][self.grid_x] > 0:
                self.layer += 1
            else:
                print("Cannot move down; no block below.")

    def draw(self):
        """Draw the player at the correct isometric position."""
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE * SCALE_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE * SCALE_SIZE // 4 - self.layer * BLOCK_SIZE * SCALE_SIZE // 2
        screen.blit(
            PLAYER_TEXTURE,
            (
                iso_x + SCREEN_WIDTH // 2 - PLAYER_SIZE // 2,
                iso_y + SCREEN_HEIGHT // 3.5 - PLAYER_SIZE // 2,
            ),
        )

# --- Game Setup ---
world = World()
player = Player(2, 2, layer=1, speed=1)  # Starting position and speed

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Movement keys
    if keys[pygame.K_UP]:
        player.move("up", world)
    if keys[pygame.K_DOWN]:
        player.move("down", world)
    if keys[pygame.K_LEFT]:
        player.move("left", world)
    if keys[pygame.K_RIGHT]:
        player.move("right", world)

    # Jumping up and down between layers
    if keys[pygame.K_SPACE]:  # Spacebar to jump up
        player.jump("up", world)
    if keys[pygame.K_LSHIFT]:  # Left Shift to move down
        player.jump("down", world)

    screen.fill(BACKGROUND_COLOR)
    world.render()
    player.draw()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
