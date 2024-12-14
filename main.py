import pygame
import sys

from modules.config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS, BLOCK_SIZE 
from modules.camera import Camera
from modules.world import World
from modules.player import Player
from modules.animated_sprite import AnimatedSprite

master_animation_list = []
animation_lengths_list = [5,5,5,5,5,5,5,5]
direction = 2
last_update_tick = py.time.get_ticks()
animation_speed = 150
current_frame = []
frame_step = []

def load_texture(path, width, height):
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

    # Load static textures
    TEXTURES = {
        "1": load_texture("assets/img/blocks/stone.png", BLOCK_SIZE, BLOCK_SIZE),
        "2": load_texture("assets/img/blocks/grass.png", BLOCK_SIZE, BLOCK_SIZE),
        "3": load_texture("assets/img/blocks/tree.png", BLOCK_SIZE, BLOCK_SIZE),
        "4": load_texture("assets/img/blocks/grass1.png", BLOCK_SIZE, BLOCK_SIZE),
        "5": load_texture("assets/img/blocks/block_5.png", BLOCK_SIZE, BLOCK_SIZE),
        "empty": None,
    }



    # Load animated sprite for block "6"
    # Assuming ARW2DSprite.png is 5 frames of 64x64 each
    TEXTURES["6"] = AnimatedSprite("assets/img/entities/ARW2DSprite2.png", 24, 24, num_frames=14, frame_delay=1.05)
    
    TEXTURES["7"] = AnimatedSprite("assets/img/entities/enemiSP.png", 68, 68, num_frames=3, frame_delay=1.19)
    TEXTURES["8"] = AnimatedSprite("assets/img/entities/player.png", 44, 44, num_frames=5, frame_delay=1.19)
    # Create world and player
    world = World("assets/maps/map.txt")
    player_start_x, player_start_y, player_layer = world.player_start_pos
    player = Player(player_start_x, player_start_y, layer=player_layer, speed=10, )

    camera = Camera()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]: # left
            dx = -1
            direction = 4
        if keys[pygame.K_d]: # right
            dx = 1
            direction = 0
        if keys[pygame.K_w]: # up
            dy = -1
            direction = 6
        if keys[pygame.K_s]: # down
            dy = 1
            direction = 2
        if dx != 0 and dx != 0: # if diagonal movement adjust the speed to 0.5
            dx *= .7071
            dy *= .7071

        player.move(dx, dy, dt, world) # load player move function with delta x, y and time

        # if the space key is pressed it will only move up 1 level
        if keys[pygame.K_SPACE] and not getattr(player, 'space_pressed', False):
            player.jump("up", world)
            player.space_pressed = True
        if not keys[pygame.K_SPACE]:
            player.space_pressed = False

        # if the shift key is pressed it will only move down 1 level
        if keys[pygame.K_LSHIFT] and not getattr(player, 'shift_pressed', False):
            player.jump("down", world)
            player.shift_pressed = True
        if not keys[pygame.K_LSHIFT]:
            player.shift_pressed = False

        # Update camera
        player_iso_x = (player.grid_x - player.grid_y) * BLOCK_SIZE // 2 + SCREEN_WIDTH // 2
        player_iso_y = (player.grid_x + player.grid_y) * BLOCK_SIZE // 4 - player.layer * BLOCK_SIZE // 2 + int(SCREEN_HEIGHT // 3.5)
        camera.update(player_iso_x, player_iso_y)

        # Update animated sprites
        if "6" in TEXTURES and isinstance(TEXTURES["6"] , AnimatedSprite):
            TEXTURES["6"] .update(dt)
            
        if "6" in TEXTURES and isinstance(TEXTURES["7"] , AnimatedSprite):
            TEXTURES["7"] .update(dt)

        # Render
        screen.fill(BACKGROUND_COLOR)
        world.render(screen, TEXTURES, camera)
        player.draw(screen, camera)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
