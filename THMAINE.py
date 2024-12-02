import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 940
BLOCK_SIZE = 22
PLAYER_SIZE = 22
SCALE_SIZE = 2  # initial scale factor
BACKGROUND_COLOR = (50, 50, 50)
ZOOM_SPEED = 0.1  # Speed of zooming in/out

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
        return pygame.transform.scale(texture, (int(width * scale_size), int(height * scale_size)))
    except pygame.error as e:
        print(f"Error loading texture {path}: {e}")
        sys.exit()

# Load textures into a dictionary
TEXTURES = {
    "1": load_texture("img/stone.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Block type 1
    "2": load_texture("img/grass.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Block type 2
    "3": load_texture("img/tree.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),   # Block type 3
    "4": load_texture("img/grass1.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Block type 4
    "5": load_texture("img/block_5.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE), # Special Block (permanent)
    "6": load_texture("img/ARW2DSprite.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE), # New Block type 6
    "empty": None,
}

PLAYER_TEXTURE = load_texture("img/player.png", PLAYER_SIZE, PLAYER_SIZE, SCALE_SIZE)

# --- Block 6 Description ---
BLOCK_6_DESCRIPTION = """
Block 6: This is a special decorative block that adds visual appeal to the world.
It is not interactable but can be used to create beautiful landscapes or structures.
It has a unique texture that resembles a mystical stone or artifact.
"""



# --- Camera Setup ---
class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height

        # Define the visible frame (e.g., a rectangle in which the player can move freely)
        self.frame_width = SCREEN_WIDTH // 2  # Adjust as needed
        self.frame_height = SCREEN_HEIGHT // 2

        # Margins from the center of the screen to define the frame boundaries
        self.margin_left = self.frame_width // 2
        self.margin_right = self.frame_width // 2
        self.margin_top = self.frame_height // 2
        self.margin_bottom = self.frame_height // 2

    def update(self, player_iso_x, player_iso_y):
        """Update the camera offset based on the player's position."""
        # Calculate the player's position on the screen
        screen_player_x = player_iso_x + self.offset_x
        screen_player_y = player_iso_y + self.offset_y

        # Check if the player is outside the frame horizontally
        if screen_player_x < self.margin_left:
            self.offset_x += self.margin_left - screen_player_x
        elif screen_player_x > SCREEN_WIDTH - self.margin_right:
            self.offset_x -= screen_player_x - (SCREEN_WIDTH - self.margin_right)

        # Check if the player is outside the frame vertically
        if screen_player_y < self.margin_top:
            self.offset_y += self.margin_top - screen_player_y
        elif screen_player_y > SCREEN_HEIGHT - self.margin_bottom:
            self.offset_y -= screen_player_y - (SCREEN_HEIGHT - self.margin_bottom)

# --- World Map Setup ---
class World:
    def __init__(self):
        self.layers = 3  # Number of layers (0, 1, 2)
        self.map_data = self.load_map_from_file("maps/map.txt")  # Load map from file
        self.player_start_pos = self.find_player_start_position()  # Find player's start position

    def load_map_from_file(self, file_path):
        """Load map from a text file with layers."""
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            chunks = []
            current_layer = -1  # Current layer index

            for line in lines:
                line = line.strip()
                if line.startswith("# Layer"):
                    current_layer += 1
                    chunks.append([])  # Start a new layer
                    continue
                if line and current_layer >= 0:
                    # Add map row to the current layer
                    # Convert each character to an integer
                    chunks[current_layer].append([int(char) for char in line])
            return chunks

        except FileNotFoundError:
            print(f"Map file {file_path} not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()

    def find_player_start_position(self):
        """Find the position of block '5' on layer 1 (second layer) to set player's start position."""
        layer_index = 1  # Second layer (since layers are 0-indexed)
        for y, row in enumerate(self.map_data[layer_index]):
            for x, block in enumerate(row):
                if block == 5:
                    return (x, y, layer_index)
        # If no block '5' found, default to (0, 0, layer_index)
        print("Block '5' not found on layer 1. Setting default player position.")
        return (0, 0, layer_index)

    def render(self, scale_size, camera):
        """Render the map layers in isometric view with current zoom level."""
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:  # Skip empty blocks
                        texture = TEXTURES.get(str(block), None)
                        if texture:
                            iso_x = (x - y) * BLOCK_SIZE * scale_size // 2
                            iso_y = (x + y) * BLOCK_SIZE * scale_size // 4 - layer_index * BLOCK_SIZE * scale_size // 2

                            # Adjust position by camera offset
                            draw_x = iso_x + SCREEN_WIDTH // 3.5 + camera.offset_x
                            draw_y = iso_y + SCREEN_HEIGHT // 4.5 + camera.offset_y

                            screen.blit(texture, (draw_x, draw_y))

# --- Player Setup ---
class Player:
    def __init__(self, x, y, layer=1, speed=5):
        self.grid_x = x
        self.grid_y = y
        self.layer = layer  # Player's current layer
        self.speed = speed  # Units per second

    def move(self, dx, dy, dt, world):
        """Move the player if possible."""
        new_x = self.grid_x + dx * self.speed * dt
        new_y = self.grid_y + dy * self.speed * dt

        # Convert positions to integers for indexing the map
        int_new_x = int(new_x)
        int_new_y = int(new_y)

        # Check map boundaries and if there's a block on the current layer
        if (
            0 <= int_new_x < len(world.map_data[self.layer][0]) and  # Check X boundaries
            0 <= int_new_y < len(world.map_data[self.layer]) and      # Check Y boundaries
            world.map_data[self.layer][int_new_y][int_new_x] > 0  # Check for a block on the current layer
        ):
            self.grid_x, self.grid_y = new_x, new_y
        else:
            print("Cannot move to that position.")

    def jump(self, direction, world):
        """Move up or down layers if possible."""
        int_x = int(self.grid_x)
        int_y = int(self.grid_y)

        if direction == "up" and self.layer > 0:
            # Attempt to move up a layer
            if world.map_data[self.layer - 1][int_y][int_x] > 0:
                self.layer -= 1
            else:
                print("Cannot jump up; no block above.")
        elif direction == "down" and self.layer < world.layers - 1:
            # Attempt to move down a layer
            if world.map_data[self.layer + 1][int_y][int_x] > 0:
                self.layer += 1
            else:
                print("Cannot move down; no block below.")

    def draw(self, scale_size, camera):
        """Draw the player at the correct isometric position."""
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE * scale_size // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE * scale_size // 4 - self.layer * BLOCK_SIZE * scale_size // 2

        # Adjust position by camera offset
        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - PLAYER_SIZE // 2
        draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y - PLAYER_SIZE // 2

        screen.blit(PLAYER_TEXTURE, (draw_x, draw_y))

# --- Game Setup ---
world = World()
player_start_x, player_start_y, player_layer = world.player_start_pos
player = Player(player_start_x, player_start_y, layer=player_layer, speed=100)  # Starting position and speed
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)  # Initialize the camera

# --- Game Loop ---
running = True
while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle zoom in/out with CTRL + mouse wheel
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                if event.button == 4:  # Scroll up (zoom in)
                    SCALE_SIZE += ZOOM_SPEED
                elif event.button == 5:  # Scroll down (zoom out)
                    SCALE_SIZE = max(0.1, SCALE_SIZE - ZOOM_SPEED)  # Prevent SCALE_SIZE from going negative

    keys = pygame.key.get_pressed()

    # Movement keys (similar to Terraria)
    dx = 0
    dy = 0
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1

    player.move(dx, dy, dt, world)

    # Jumping up and down between layers
    if keys[pygame.K_SPACE]:  # Spacebar to jump up
        player.jump("up", world)
    if keys[pygame.K_LSHIFT]:  # Left Shift to move down
        player.jump("down", world)

    # Update camera position based on player's isometric position
    player_iso_x = (player.grid_x - player.grid_y) * BLOCK_SIZE * SCALE_SIZE // 2 + SCREEN_WIDTH // 2
    player_iso_y = (player.grid_x + player.grid_y) * BLOCK_SIZE * SCALE_SIZE // 4 - player.layer * BLOCK_SIZE * SCALE_SIZE // 2 + SCREEN_HEIGHT // 3.5
    camera.update(player_iso_x, player_iso_y)

    screen.fill(BACKGROUND_COLOR)
    world.render(SCALE_SIZE, camera)  # Pass the camera to the render method
    player.draw(SCALE_SIZE, camera)

    pygame.display.flip()
    # clock.tick(60)  # Already handled above

pygame.quit()
sys.exit()
