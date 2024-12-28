import pygame

# Screen and scaling
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 940
BLOCK_SIZE = 32
PLAYER_SIZE = 32

# Colors
BACKGROUND_COLOR = (50, 50, 50)

# Framerate
FPS = 160
SOLID_BLOCKS = {1, 2, 3, 4, 5, 6, 7, 34, 463, 999}  # anything you want
############    ---------    If the block’s ID is in this set, the player cannot walk there.
# Set up pygame font if needed
pygame.font.init()
