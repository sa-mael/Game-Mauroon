import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 940
BLOCK_SIZE = 22
PLAYER_SIZE = 22
SCALE_SIZE = 2  # Initial scale factor
ZOOM_SPEED = 0.1  # Speed of zooming in/out
BACKGROUND_COLOR = (50, 50, 50)

# --- Initialize pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric World with Animation")
clock = pygame.time.Clock()

# --- AnimatedSprite Class ---
class AnimatedSprite:
    def __init__(self, image_path, frame_width, frame_height, scale_size, num_frames, frame_delay):
        """
        Loads an animated sprite from a sprite sheet and allows frame-by-frame animation.
        
        :param image_path: Path to the sprite sheet image.
        :param frame_width: Width of a single frame.
        :param frame_height: Height of a single frame.
        :param scale_size: Scaling factor for the sprite.
        :param num_frames: Number of frames in the animation.
        :param frame_delay: Time between frames in seconds.
        """
        try:
            self.sheet = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading animated sprite '{image_path}': {e}")
            sys.exit()
        
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale_size = scale_size
        self.num_frames = num_frames
        self.frame_delay = frame_delay

        self.frames = []
        self.current_frame = 0
        self.elapsed_time = 0  # Time since last frame change

        # Extract frames from the sprite sheet
        for i in range(self.num_frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            try:
                frame = self.sheet.subsurface(rect)
            except ValueError:
                print(f"Error: Frame {i} is outside the sprite sheet bounds.")
                sys.exit()
            scaled_frame = pygame.transform.scale(
                frame,
                (int(self.frame_width * self.scale_size), int(self.frame_height * self.scale_size))
            )
            self.frames.append(scaled_frame)

    def update(self, dt):
        """
        Updates the animation frame based on elapsed time.
        
        :param dt: Delta time since last update (in seconds).
        """
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, surface, x, y):
        """
        Draws the current frame of the animation at the specified position.
        
        :param surface: Pygame surface to draw on.
        :param x: X-coordinate.
        :param y: Y-coordinate.
        """
        surface.blit(self.frames[self.current_frame], (x, y))


# --- Camera Class ---
class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

        # Define the visible frame (e.g., a rectangle in which the player can move freely)
        self.frame_width = SCREEN_WIDTH // 2  # Adjust as needed
        self.frame_height = SCREEN_HEIGHT // 2

        # Margins from the center of the screen to define the frame boundaries
        self.margin_left = self.frame_width // 2
        self.margin_right = self.frame_width // 2
        self.margin_top = self.frame_height // 2
        self.margin_bottom = self.frame_height // 2

    def update(self, player_iso_x, player_iso_y):
        """
        Updates the camera offset based on the player's position.
        
        :param player_iso_x: Player's isometric X position.
        :param player_iso_y: Player's isometric Y position.
        """
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


# --- World Class ---
class World:
    def __init__(self, map_file):
        self.layers = 3  # Number of layers (0, 1, 2)
        self.map_data = self.load_map_from_file(map_file)  # Load map from file
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
                    chunks[current_layer].append([int(char) for char in line])
            return chunks

        except FileNotFoundError:
            print(f"Map file '{file_path}' not found!")
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

    def render(self, surface, textures, camera):
        """Render the map layers in isometric view with current zoom level."""
        for layer_index, layer in enumerate(self.map_data):
            for y, row in enumerate(layer):
                for x, block in enumerate(row):
                    if block > 0:
                        if block == 6 and isinstance(textures["6"], AnimatedSprite):
                            # Animated block
                            iso_x = (x - y) * BLOCK_SIZE * SCALE_SIZE // 2
                            iso_y = (x + y) * BLOCK_SIZE * SCALE_SIZE // 4 - layer_index * BLOCK_SIZE * SCALE_SIZE // 2

                            # Adjust position by camera offset
                            draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                            draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y

                            textures["6"].draw(surface, draw_x, draw_y)
                        else:
                            # Static blocks
                            texture = textures.get(str(block), None)
                            if texture:
                                iso_x = (x - y) * BLOCK_SIZE * SCALE_SIZE // 2
                                iso_y = (x + y) * BLOCK_SIZE * SCALE_SIZE // 4 - layer_index * BLOCK_SIZE * SCALE_SIZE // 2

                                # Adjust position by camera offset
                                draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x
                                draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y

                                surface.blit(texture, (draw_x, draw_y))


# --- Player Class ---
class Player:
    def __init__(self, x, y, layer=1, speed=5, texture_path="img/player.png"):
        self.grid_x = x
        self.grid_y = y
        self.layer = layer  # Player's current layer
        self.speed = speed  # Units per second

        # Load player texture
        try:
            self.texture = pygame.image.load(texture_path).convert_alpha()
            self.texture = pygame.transform.scale(self.texture, (PLAYER_SIZE, PLAYER_SIZE))
        except pygame.error as e:
            print(f"Error loading player texture '{texture_path}': {e}")
            sys.exit()

    def move(self, dx, dy, dt, world):
        """Move the player if possible."""
        new_x = self.grid_x + dx * self.speed * dt
        new_y = self.grid_y + dy * self.speed * dt

        # Convert positions to integers for indexing the map
        int_new_x = int(new_x)
        int_new_y = int(new_y)

        # Check map boundaries and if there's a block on the current layer
        if (
            0 <= int_new_x < len(world.map_data[self.layer][0]) and
            0 <= int_new_y < len(world.map_data[self.layer]) and
            world.map_data[self.layer][int_new_y][int_new_x] > 0
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

    def draw(self, surface, camera):
        """Draw the player at the correct isometric position."""
        iso_x = (self.grid_x - self.grid_y) * BLOCK_SIZE * SCALE_SIZE // 2
        iso_y = (self.grid_x + self.grid_y) * BLOCK_SIZE * SCALE_SIZE // 4 - self.layer * BLOCK_SIZE * SCALE_SIZE // 2

        # Adjust position by camera offset
        draw_x = iso_x + SCREEN_WIDTH // 2 + camera.offset_x - PLAYER_SIZE // 2
        draw_y = iso_y + SCREEN_HEIGHT // 3.5 + camera.offset_y - PLAYER_SIZE // 2

        surface.blit(self.texture, (draw_x, draw_y))


# --- Load Static Textures Function ---
def load_texture(path, width, height, scale_size):
    """Load and scale a texture."""
    try:
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, (int(width * scale_size), int(height * scale_size)))
    except pygame.error as e:
        print(f"Error loading texture '{path}': {e}")
        sys.exit()


# --- Main Game Setup ---
def main():
    global SCALE_SIZE  # Объявление глобальной переменной

    # --- Load Static Textures ---
    TEXTURES = {
        "1": load_texture("img/stone.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),    # Block type 1
        "2": load_texture("img/grass.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),    # Block type 2
        "3": load_texture("img/tree.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),     # Block type 3
        "4": load_texture("img/grass1.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),   # Block type 4
        "5": load_texture("img/block_5.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE),  # Block type 5
        "empty": None,
    }

    # --- Load Animated Sprite for Block 6 ---
    # Убедитесь, что 'img/ARW2DSprite.png' существует и имеет 5 кадров по горизонтали, каждый 64x64 пикселя
    TEXTURES["6"] = AnimatedSprite("img/ARW2DSprite.png", 64, 64, SCALE_SIZE, num_frames=5, frame_delay=0.1)

    # --- Create World ---
    world = World("maps/map.txt")
    player_start_x, player_start_y, player_layer = world.player_start_pos
    player = Player(player_start_x, player_start_y, layer=player_layer, speed=100, texture_path="img/player.png")  # Starting position and speed

    # --- Initialize Camera ---
    camera = Camera()

    # --- Game Loop ---
    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle zoom in/out with CTRL + mouse wheel
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                    if event.button == 4:  # Scroll up (zoom in)
                        SCALE_SIZE += ZOOM_SPEED
                        # Update all static textures
                        for key in TEXTURES:
                            if key != "6" and TEXTURES[key]:
                                try:
                                    TEXTURES[key] = load_texture(f"img/{key}.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE)
                                except:
                                    pass  # Если файл не найден или другая ошибка, пропустим
                    elif event.button == 5:  # Scroll down (zoom out)
                        SCALE_SIZE = max(0.1, SCALE_SIZE - ZOOM_SPEED)  # Prevent SCALE_SIZE from going negative
                        # Update all static textures
                        for key in TEXTURES:
                            if key != "6" and TEXTURES[key]:
                                try:
                                    TEXTURES[key] = load_texture(f"img/{key}.png", BLOCK_SIZE, BLOCK_SIZE, SCALE_SIZE)
                                except:
                                    pass  # Если файл не найден или другая ошибка, пропустим

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
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

        # Update animated sprites
        if isinstance(TEXTURES["6"], AnimatedSprite):
            TEXTURES["6"].update(dt)

        # Render everything
        screen.fill(BACKGROUND_COLOR)
        world.render(screen, TEXTURES, camera)  # Render the world
        player.draw(screen, camera)             # Draw the player

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
