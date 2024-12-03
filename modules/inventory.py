# modules/inventory.py

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from items import Item

class Inventory:
    def __init__(self, width=5, height=4):
        """
        Initializes the player's inventory.

        :param width: Number of slots horizontally.
        :param height: Number of slots vertically.
        """
        self.width = width
        self.height = height
        self.slots = [[None for _ in range(width)] for _ in range(height)]
        self.selected_slot = (0, 0)  # Currently selected slot

        # Load inventory slot graphics
        try:
            self.slot_image = pygame.image.load("assets/img/ui/inventory_slot.png").convert_alpha()
            self.slot_image = pygame.transform.scale(self.slot_image, (50, 50))
        except pygame.error as e:
            print(f"Error loading inventory slot image: {e}")
            sys.exit()

    def add_item(self, item):
        """
        Adds an item to the first available inventory slot.

        :param item: Item object to add.
        :return: True if added successfully, False if inventory is full.
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.slots[y][x] is None:
                    self.slots[y][x] = item
                    return True
        return False  # Inventory is full

    def remove_item(self, x, y):
        """
        Removes an item from the specified slot.

        :param x: X-coordinate of the slot.
        :param y: Y-coordinate of the slot.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.slots[y][x] = None

    def draw(self, surface):
        """
        Draws the inventory on the screen.

        :param surface: Pygame surface to draw on.
        """
        for y in range(self.height):
            for x in range(self.width):
                draw_x = 50 + x * 60
                draw_y = SCREEN_HEIGHT - (self.height - y) * 60
                surface.blit(self.slot_image, (draw_x, draw_y))
                if self.slots[y][x]:
                    # Draw the item in the slot
                    surface.blit(self.slots[y][x].image, (draw_x + 5, draw_y + 5))
