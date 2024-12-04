# modules/items.py

import pygame
import sys

class Item:
    def __init__(self, name, image_path, quantity=1):
        """
        Initializes an item.

        :param name: The name of the item.
        :param image_path: Path to the item's image.
        :param quantity: Quantity of the item.
        """
        self.name = name
        self.quantity = quantity

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))  # Scale icon size
        except pygame.error as e:
            print(f"Error loading item image '{image_path}': {e}")
            sys.exit()

    def __repr__(self):
        return f"Item(name={self.name}, quantity={self.quantity})"
