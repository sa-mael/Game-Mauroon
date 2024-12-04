# modules/inventory.py

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from modules.items import Item


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
        self.visible = False  # Inventory visibility

        # Load inventory slot graphics
        try:
            self.slot_image = pygame.image.load("assets/img/ui/inventory_slot.png").convert_alpha()
            self.slot_image = pygame.transform.scale(self.slot_image, (50, 50))
        except pygame.error as e:
            print(f"Error loading inventory slot image: {e}")
            # Create a simple placeholder surface if image is missing
            self.slot_image = pygame.Surface((50, 50))
            self.slot_image.fill((100, 100, 100))  # Grey color

    def toggle_visibility(self):
        """Toggle the visibility of the inventory."""
        self.visible = not self.visible

    def add_item(self, item):
        """
        Adds an item to the first available inventory slot.

        :param item: Item object to add.
        :return: True if added successfully, False if inventory is full.
        """
        for y in range(self.height):
            for x in range(self.width):
                existing_item = self.slots[y][x]
                if existing_item and existing_item.name == item.name:
                    existing_item.quantity += item.quantity
                    return True
                elif self.slots[y][x] is None:
                    self.slots[y][x] = item
                    return True
        return False  # Inventory is full

    def remove_item(self, item_name, quantity):
        """
        Removes a specific quantity of an item from the inventory.

        :param item_name: The name of the item to remove.
        :param quantity: The quantity to remove.
        :return: True if removal was successful, False otherwise.
        """
        for y in range(self.height):
            for x in range(self.width):
                item = self.slots[y][x]
                if item and item.name == item_name:
                    if item.quantity > quantity:
                        item.quantity -= quantity
                        return True
                    elif item.quantity == quantity:
                        self.slots[y][x] = None
                        return True
                    else:
                        print(f"Not enough '{item_name}' to remove.")
                        return False
        print(f"Item '{item_name}' not found in inventory.")
        return False

    def has_item(self, item_name, quantity):
        """
        Checks if the inventory has at least a certain quantity of an item.

        :param item_name: The name of the item to check.
        :param quantity: The required quantity.
        :return: True if the inventory has enough, False otherwise.
        """
        total = 0
        for row in self.slots:
            for item in row:
                if item and item.name == item_name:
                    total += item.quantity
                    if total >= quantity:
                        return True
        return False

    def draw(self, surface):
        """
        Draws the inventory on the screen if it's visible.

        :param surface: Pygame surface to draw on.
        """
        if not self.visible:
            return

        inventory_width = self.width * 60 + 50
        inventory_height = self.height * 60 + 50
        inventory_surface = pygame.Surface((inventory_width, inventory_height), pygame.SRCALPHA)
        inventory_surface.fill((0, 0, 0, 150))  # Semi-transparent background

        for y in range(self.height):
            for x in range(self.width):
                draw_x = 25 + x * 60
                draw_y = 25 + y * 60
                inventory_surface.blit(self.slot_image, (draw_x, draw_y))
                if self.slots[y][x]:
                    # Draw the item in the slot
                    inventory_surface.blit(self.slots[y][x].image, (draw_x + 5, draw_y + 5))
                    # Draw quantity
                    font = pygame.font.SysFont(None, 24)
                    quantity_text = font.render(str(self.slots[y][x].quantity), True, (255, 255, 255))
                    inventory_surface.blit(quantity_text, (draw_x + 35, draw_y + 35))

        # Blit the inventory surface to the main screen
        surface.blit(inventory_surface, (SCREEN_WIDTH // 2 - inventory_width // 2, SCREEN_HEIGHT // 2 - inventory_height // 2))
