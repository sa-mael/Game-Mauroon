import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 940
BLOCK_SIZE = 22
PLAYER_SIZE = 22
SCALE_SIZE = 2  # initial scale factor
ZOOM_SPEED = 0.1  # Speed of zooming in/out
BACKGROUND_COLOR = (50, 50, 50)

# --- Initialize pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game with Animated Sprite")
clock = pygame.time.Clock()

# --- AnimatedSprite Class ---
class AnimatedSprite:
    def __init__(self, image_path, frame_width, frame_height, scale_size, num_frames, frame_delay):
        self.sheet = pygame.image.load(image_path).convert_alpha()  # Загрузите изображение
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale_size = scale_size
        self.num_frames = num_frames
        self.frame_delay = frame_delay

        self.frames = []
        self.current_frame = 0
        self.elapsed_time = 0  # Время, прошедшее для задержки

        # Убедитесь, что изображения корректно обрезаются
        for i in range(self.num_frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            self.frames.append(self.sheet.subsurface(rect))  # Вырезаем кадры

    def update(self, dt):
        """Обновляем анимацию."""
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, x, y):
        """Отображаем текущий кадр анимации на экране."""
        scaled_frame = pygame.transform.scale(self.frames[self.current_frame], 
                                               (int(self.frame_width * self.scale_size), 
                                                int(self.frame_height * self.scale_size)))
        screen.blit(scaled_frame, (x, y))  # Отображаем кадр


# --- World Class ---
class World:
    def __init__(self, special_block_positions=None):
        self.layers = 3  # Number of layers (0, 1, 2)
        self.map_data = self.load_map_from_file("maps/map.txt")  # Load map from file
        if special_block_positions is None:
            self.special_block_positions = []  # List to hold positions of block 5
        else:
            self.special_block_positions = special_block_positions  # List of tuples (x, y, layer)

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
                    chunks[current_layer].append([int(char) for char in line])
            return chunks

        except FileNotFoundError:
            print(f"Map file {file_path} not found!")
            sys.exit()
        except Exception as e:
            print(f"Error loading map: {e}")
            sys.exit()

    def render(self, scale_size):
        """Render the map layers in isometric view with current zoom level."""
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:  # Skip empty blocks
                        texture = TEXTURES.get(str(block), None)
                        if texture:
                            iso_x = (x - y) * BLOCK_SIZE * scale_size // 2
                            iso_y = (x + y) * BLOCK_SIZE * scale_size // 4 - layer_index * BLOCK_SIZE * scale_size // 2
                            screen.blit(texture, (iso_x + SCREEN_WIDTH // 3.5, iso_y + SCREEN_HEIGHT // 4.5))


# --- Player Class ---
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

    def draw(self, scale_size):
        """Draw the player at the correct isometric position."""
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE * scale_size // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE * scale_size // 4 - self.layer * BLOCK_SIZE * scale_size // 2
        screen.blit(
            PLAYER_TEXTURE,
            (
                iso_x + SCREEN_WIDTH // 2 - PLAYER_SIZE // 2,
                iso_y + SCREEN_HEIGHT // 3.5 - PLAYER_SIZE // 2,
            ),
        )


# --- Game Setup ---
TEXTURES = {
    "1": load_texture("img/stone.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Block type 1
    "2": load_texture("img/grass.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Block type 2
    "3": load_texture("img/tree.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),   # Block type 3
    "4": load_texture("img/grass1.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Block type 4
    "5": load_texture("img/block_5.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE), # Special Block (permanent)
    "empty": None,
}

# Add Animated Sprite for Block 6 (with 5 frames of animation)
SCALE_SIZE = 2
frame_width = 64
frame_height = 64
num_frames = 5
frame_delay = 0.1  # Delay between frames
ARW2DSprite = AnimatedSprite("img/ARW2DSprite.png", frame_width, frame_height, SCALE_SIZE, num_frames, frame_delay)
TEXTURES["6"] = ARW2DSprite  # Add animated sprite as block 6

# Create world and player
special_block_positions = [
    (5, 5, 1),  # Block 5 at position x=5, y=5, layer=1
    (7, 8, 0),  # Block 5 at position x=7, y=8, layer=0
]
world = World(special_block_positions)
player = Player(10, 10)

# --- Game Loop ---
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    screen.fill(BACKGROUND_COLOR)  # Fill background with a color
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw animated sprite (ARW2DSprite)
    ARW2DSprite.update(dt)  # Update sprite animation
    ARW2DSprite.draw(100, 100)  # Draw the sprite at position (100, 100)

    # Update and draw world and player
    world.render(SCALE_SIZE)  # Render the world with current scale
    player.draw(SCALE_SIZE)  # Draw the player

    pygame.display.flip()

pygame.quit()
sys.exit()
