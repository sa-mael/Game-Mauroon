# main.py

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_SIZE, BACKGROUND_COLOR, FPS
from modules.camera import Camera
from modules.world import World
from modules.player import Player
from modules.block import Block
from modules.animated_sprite import AnimatedSprite

# Initialize pygame
pygame.init()

# Set up the display surface and the game clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Isometric World")
clock = pygame.time.Clock()

# Set up the camera
camera = Camera(SCALE_SIZE)

# Initialize the world
world = World()

# Initialize the player at the start position (x, y, layer)
player = Player(2, 2, 1)

# Load textures and sprites (assuming you have a function to do this)
textures = {
    "1": pygame.image.load("assets/img/blocks/stone.png"),
    "2": pygame.image.load("assets/img/blocks/grass.png"),
    "3": pygame.image.load("assets/img/blocks/tree.png"),
    "6": AnimatedSprite("assets/img/blocks/ARW2DSprite.png", 64, 64, SCALE_SIZE, num_frames=5, frame_delay=0.1),
    "player": pygame.image.load("assets/img/blocks/player.png"),  # Make sure this file exists
}

# Main game loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Time delta for smooth movement

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input (player movement, camera zoom, etc.)
    keys = pygame.key.get_pressed()
    player.move(keys, dt, world)
    player.update_animation()

    # Render the world and player
    screen.fill(BACKGROUND_COLOR)
    world.render(screen, textures, camera)
    player.draw(screen, textures)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
