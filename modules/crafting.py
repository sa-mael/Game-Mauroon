# modules/crafting.py

import json
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from .items import Item  # Corrected relative import

class Crafting:
    def __init__(self, recipes_file):
        self.recipes = self.load_recipes(recipes_file)

    def load_recipes(self, file_path):
        """
        Loads crafting recipes from a JSON file.

        :param file_path: Path to the recipes JSON file.
        :return: Dictionary of recipes.
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Recipes file '{file_path}' not found!")
            sys.exit()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from '{file_path}': {e}")
            sys.exit()

    def craft(self, item_name, inventory):
        """
        Attempts to craft an item using the inventory.

        :param item_name: The name of the item to craft.
        :param inventory: The player's Inventory object.
        """
        recipe = self.recipes.get(item_name, None)
        if not recipe:
            print(f"No recipe found for '{item_name}'.")
            return

        # Check if all required items are present
        for ingredient, qty in recipe['ingredients'].items():
            if not inventory.has_item(ingredient, qty):
                print(f"Not enough '{ingredient}' to craft '{item_name}'.")
                return

        # Remove the ingredients from inventory
        for ingredient, qty in recipe['ingredients'].items():
            inventory.remove_item(ingredient, qty)

        # Add the crafted item to inventory
        crafted_item = Item(name=item_name, image_path=recipe['result_image'], quantity=1)
        if inventory.add_item(crafted_item):
            print(f"Crafted '{item_name}' successfully!")
        else:
            print(f"Failed to add '{item_name}' to inventory. Inventory might be full.")
