# main.py
import pygame
import sys

# --- Import your isometric modules ---
from modules.config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS, BLOCK_SIZE
from modules.camera import Camera
from modules.world import World
from modules.player import Player
from modules.animated_sprite import AnimatedSprite

# --- Import the UI menu system and optional game wrapper ---
from ui.menu import Menu

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
    pygame.display.set_caption("Isometric World with Menu")
    clock = pygame.time.Clock()

    # -----------------------------------------------------
    # 1) MENU STATE SETUP
    # -----------------------------------------------------
    menu_active = True
    game_active = False
    menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)

    # -----------------------------------------------------
    # 2) GAME STATE SETUP
    # -----------------------------------------------------
    # Load static textures
    TEXTURES = {
        "1": load_texture("assets/img/blocks/stone.png",  BLOCK_SIZE, BLOCK_SIZE),
        "2": load_texture("assets/img/blocks/lite stone.png",  BLOCK_SIZE, BLOCK_SIZE),
        "3": load_texture("assets/img/blocks/hard grass.png",  BLOCK_SIZE, BLOCK_SIZE),
        "4": load_texture("assets/img/blocks/grass.png",   BLOCK_SIZE, BLOCK_SIZE),
        "5": load_texture("assets/img/blocks/clear water.png", BLOCK_SIZE, BLOCK_SIZE),
        "6": load_texture("assets/img/blocks/grass lo.png",BLOCK_SIZE, BLOCK_SIZE),
        "7": load_texture("assets/img/blocks/flowers.png", 44,88 ),
        "8": load_texture("assets/img/blocks/trea.png",44, 88),
        "9": load_texture("assets/img/blocks/light wood.png",44, 88),
        "10": load_texture("assets/img/blocks/ tall grass.png",BLOCK_SIZE, BLOCK_SIZE),
        
        "empty": None,
    }

    # Load animated sprites
    TEXTURES["6"] = AnimatedSprite(
        "assets/img/blocks/ARW2DSprite2.png",
        frame_width=24,
        frame_height=24,
        num_frames=14,
        frame_delay=1.05
    )

    TEXTURES["7"] = AnimatedSprite(
        "assets/img/enemies/enemiSP.png",
        frame_width=68,
        frame_height=68,
        num_frames=3,
        frame_delay=1.19
    )

    # Create the world and player
    world = World("assets/maps/generated_map.txt")
    player_start_x, player_start_y, player_layer = world.player_start_pos
    player = Player(
        x=player_start_x,
        y=player_start_y,
        layer=player_layer,
        speed=10,
        texture_path="assets/img/blocks/player.png"
    )

    camera = Camera()

    # -----------------------------------------------------
    # 3) MAIN LOOP
    # -----------------------------------------------------
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- MENU EVENTS ---
            if menu_active:
                menu.handle_event(event)
                # If user clicked "Continue", we move to the game state
                if menu.start_game:
                    menu_active = False
                    game_active = True

        # -------------------------------------------------
        # MENU MODE
        # -------------------------------------------------
        if menu_active:
            # We can update menu animations (if any)
            menu.update(dt)

            # Draw the menu
            screen.fill((30, 30, 30))  # Dark background for the menu
            menu.draw(screen)
            pygame.display.flip()
            continue  # Skip the rest of the loop (game logic)

        # -------------------------------------------------
        # GAME MODE
        # -------------------------------------------------
        if game_active:
            # --- Handle game input ---
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

            # Update camera based on player's isometric position
            player_iso_x = (player.grid_x - player.grid_y) * BLOCK_SIZE // 2 + SCREEN_WIDTH // 2
            player_iso_y = (
                (player.grid_x + player.grid_y) * BLOCK_SIZE // 4
                - player.layer * BLOCK_SIZE // 2
                + int(SCREEN_HEIGHT // 3.5)
            )
            camera.update(player_iso_x, player_iso_y)

            # Update animated sprites
            if "6" in TEXTURES and isinstance(TEXTURES["6"], AnimatedSprite):
                TEXTURES["6"].update(dt)
            if "7" in TEXTURES and isinstance(TEXTURES["7"], AnimatedSprite):
                TEXTURES["7"].update(dt)

            # --- Render the game ---
            screen.fill(BACKGROUND_COLOR)
            world.render(screen, TEXTURES, camera)
            player.draw(screen, camera)

            pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
