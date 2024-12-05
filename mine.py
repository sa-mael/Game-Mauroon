# mine.py

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_SIZE, ZOOM_SPEED, BACKGROUND_COLOR, FPS
from modules.animated_sprite import AnimatedSprite
from modules.camera import Camera
from modules.world import World
from modules.player import Player
from modules.inventory import Inventory
from modules.crafting import Crafting
from modules.enemies import Enemy
from modules.ui import HealthBar
from modules.items import Item

def load_texture(path, width, height, scale_size):
    """Loads and scales a texture."""
    try:
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, (int(width * scale_size), int(height * scale_size)))
    except pygame.error as e:
        print(f"Error loading texture '{path}': {e}")
        sys.exit()

def main():
    # --- Initialize Pygame ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Isometric World with Terraria Mechanics")
    clock = pygame.time.Clock()

    # --- Load Static Textures ---
    TEXTURES = {
        "1": load_texture("assets/img/blocks/stone.png", 22, 22, SCALE_SIZE),    # Block type 1
        "2": load_texture("assets/img/blocks/grass.png", 22, 22, SCALE_SIZE),    # Block type 2
        "3": load_texture("assets/img/blocks/tree.png", 22, 22, SCALE_SIZE),     # Block type 3
        "4": load_texture("assets/img/blocks/grass1.png", 22, 22, SCALE_SIZE),   # Block type 4
        "5": load_texture("assets/img/blocks/block_5.png", 22, 22, SCALE_SIZE),  # Block type 5
        "empty": None,
    }

    # --- Load Animated Sprite for Block 6 ---
    TEXTURES["6"] = AnimatedSprite(
        image_path="assets/img/blocks/ARW2DSprite.png",
        num_frames=5,
        frame_delay=0.1
    )

    # --- Create World ---
    world = World("assets/maps/map.txt")

    # --- Create Player ---
    player_start_x, player_start_y, player_layer = world.player_start_pos
    player = Player(
        x=player_start_x,
        y=player_start_y,
        layer=player_layer,
        speed=100,
        texture_path="assets/img/blocks/player.png"
    )

    # --- Create Camera ---
    camera = Camera()

    # --- Create Inventory and Crafting System ---
    inventory = Inventory(width=5, height=4)
    crafting = Crafting(recipes_file="data/recipes.json")

    # --- Create Health Bar ---
    health_bar = HealthBar(max_health=100, current_health=100)

    # --- Create Enemies ---
    enemies = [
        Enemy(x=10, y=15, image_path="assets/img/enemies/zombie.png", speed=60),
        Enemy(x=20, y=25, image_path="assets/img/enemies/skeleton.png", speed=50)
        # Add more enemies as needed
    ]

    # --- Main Game Loop ---
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds

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
                                TEXTURES[key] = pygame.transform.scale(
                                    pygame.image.load(f"assets/img/blocks/{key}.png").convert_alpha(),
                                    (int(22 * SCALE_SIZE), int(22 * SCALE_SIZE))
                                )
                    elif event.button == 5:  # Scroll down (zoom out)
                        SCALE_SIZE = max(0.1, SCALE_SIZE - ZOOM_SPEED)  # Prevent SCALE_SIZE from going negative
                        # Update all static textures
                        for key in TEXTURES:
                            if key != "6" and TEXTURES[key]:
                                TEXTURES[key] = pygame.transform.scale(
                                    pygame.image.load(f"assets/img/blocks/{key}.png").convert_alpha(),
                                    (int(22 * SCALE_SIZE), int(22 * SCALE_SIZE))
                                )

            # Handle crafting and inventory toggling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Press 'C' to craft
                    # Example: Craft a Sword
                    crafting.craft("Sword", inventory)
                elif event.key == pygame.K_i:  # Press 'I' to toggle inventory
                    inventory.toggle_visibility()

        # Handle player movement
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

        # Handle jumping between layers
        if keys[pygame.K_SPACE]:  # Press Spacebar to jump up
            player.jump("up", world)
        if keys[pygame.K_LSHIFT]:  # Press Left Shift to jump down
            player.jump("down", world)

        # Update camera position based on player's isometric position
        player_iso_x = (player.grid_x - player.grid_y) * 22 * SCALE_SIZE // 2 + SCREEN_WIDTH // 2
        player_iso_y = (player.grid_x + player.grid_y) * 22 * SCALE_SIZE // 4 - player.layer * 22 * SCALE_SIZE // 2 + SCREEN_HEIGHT // 3.5
        camera.update(player_iso_x, player_iso_y)

        # Update animated sprites
        if isinstance(TEXTURES["6"], AnimatedSprite):
            TEXTURES["6"].update(dt)

        # Update enemies
        for enemy in enemies:
            enemy.move_towards_player(player, dt)
            # Simple collision detection between player and enemy
            if int(enemy.grid_x) == int(player.grid_x) and int(enemy.grid_y) == int(player.grid_y):
                health_bar.update(damage=10)
                print("Player hit by enemy!")

        # Render everything
        screen.fill(BACKGROUND_COLOR)
        world.render(screen, TEXTURES, camera)
        player.draw(screen, camera)

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen, camera)

        # Draw inventory and UI
        inventory.draw(screen)
        health_bar.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
