# block.py
import pygame , sys

class Block:
    def __init__(self, block_id, image_path):
        self.id = block_id
        self.image = pygame.image.load(image_path)

    def get_image(self):
        return self.image
