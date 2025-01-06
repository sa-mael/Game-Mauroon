# main.py
import pygame
import sys

# Import from our modules folder
from modules.config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS, BLOCK_SIZE
from modules.camera import Camera
from modules.world import World
from modules.player import Player
from modules.animated_sprite import AnimatedSprite

def load_texture(path, width, height):
    """
    Load and scale a static texture from an image file.
    """
    try:
        texture = pygame.image.load(path).convert_alpha()
        texture = pygame.transform.scale(texture, (width, height))
        return texture
    except pygame.error as e:
        print(f"Error loading texture '{path}': {e}")
        sys.exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Isometric World with Animation")
    clock = pygame.time.Clock()

    # --- Load static textures ---
    TEXTURES = {
        "1": load_texture("assets/img/blocks/stone.png", BLOCK_SIZE, BLOCK_SIZE),
        "2": load_texture("assets/img/blocks/grass.png", BLOCK_SIZE, BLOCK_SIZE),
        "3": load_texture("assets/img/blocks/tree.png",  BLOCK_SIZE, BLOCK_SIZE),
        "4": load_texture("assets/img/blocks/grass1.png", BLOCK_SIZE, BLOCK_SIZE),
        "5": load_texture("assets/img/blocks/block_5.png", BLOCK_SIZE, BLOCK_SIZE),
        "empty": None,
    }

    # --- Load Animated Sprites ---
    # Block "6" uses ARW2DSprite2.png (14 frames, each 24x24)
    TEXTURES["6"] = AnimatedSprite(
        "assets/img/blocks/ARW2DSprite2.png",
        frame_width=24,
        frame_height=24,
        num_frames=14,
        frame_delay=1.05
    )

    # Block "7" uses enemiSP.png (3 frames, each 68x68)
    TEXTURES["7"] = AnimatedSprite(
        "assets/img/enemies/enemiSP.png",
        frame_width=68,
        frame_height=68,
        num_frames=3,
        frame_delay=1.19
    )

    # --- Create World and Player ---
    world = World("assets/maps/map.txt")
    player_start_x, player_start_y, player_layer = world.player_start_pos
    player = Player(
        player_start_x,
        player_start_y,
        layer=player_layer,
        speed=10,
        texture_path="assets/img/blocks/player.png"
    )

    camera = Camera()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Handle Keyboard Input ---
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

        # Move the player
        player.move(dx, dy, dt, world)

        # Jump between layers
        if keys[pygame.K_SPACE]:
            player.jump("up", world)
        if keys[pygame.K_LSHIFT]:
            player.jump("down", world)

        # --- Update Camera ---
        # Convert player's grid coords to isometric coords
        player_iso_x = (player.grid_x - player.grid_y) * BLOCK_SIZE // 2 + SCREEN_WIDTH // 2
        player_iso_y = (
            (player.grid_x + player.grid_y) * BLOCK_SIZE // 4
            - player.layer * BLOCK_SIZE // 2
            + int(SCREEN_HEIGHT // 3.5)
        )
        camera.update(player_iso_x, player_iso_y)

        # --- Update Animated Sprites ---
        if "6" in TEXTURES and isinstance(TEXTURES["6"], AnimatedSprite):
            TEXTURES["6"].update(dt)

        # Make sure we check "7" in TEXTURES, not "6"
        if "7" in TEXTURES and isinstance(TEXTURES["7"], AnimatedSprite):
            TEXTURES["7"].update(dt)

        # --- Render ---
        screen.fill(BACKGROUND_COLOR)
        world.render(screen, TEXTURES, camera)
        player.draw(screen, camera)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
