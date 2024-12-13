# modules/crafting.py

import json
from modules.items import Item

class Crafting:
    def __init__(self, recipes_file="data/recipes.json"):
        """
        Initializes the crafting system based on a recipes JSON file.

        :param recipes_file: Path to the JSON file containing crafting recipes.
        """
        try:
            with open(recipes_file, "r") as f:
                self.recipes = json.load(f)
        except FileNotFoundError:
            print(f"Recipes file '{recipes_file}' not found!")
            self.recipes = {}
        except json.JSONDecodeError as e:
            print(f"Error parsing recipes JSON file: {e}")
            self.recipes = {}

    def get_recipe(self, item_name):
        """
        Retrieves the recipe for a specific item.

        :param item_name: The name of the item to craft.
        :return: A dictionary containing the ingredients and the result, or None if not found.
        """
        return self.recipes.get(item_name, None)

    def craft(self, item_name, inventory):
        """
        Attempts to craft an item using the player's inventory.

        :param item_name: The name of the item to craft.
        :param inventory: The player's Inventory object.
        :return: True if crafting was successful, False otherwise.
        """
        recipe = self.get_recipe(item_name)
        if not recipe:
            print(f"Recipe for '{item_name}' not found.")
            return False

        # Check if the player has all required ingredients
        for ingredient in recipe["ingredients"]:
            if not inventory.has_item(ingredient["name"], ingredient["quantity"]):
                print(f"Not enough '{ingredient['name']}' to craft '{item_name}'.")
                return False

        # Remove the ingredients from the inventory
        for ingredient in recipe["ingredients"]:
            inventory.remove_item(ingredient["name"], ingredient["quantity"])

        # Add the crafted item to the inventory
        crafted_item = Item(
            name=recipe["result"]["name"],
            image_path=recipe["result"]["image"],
            quantity=1
        )
        success = inventory.add_item(crafted_item)
        if success:
            print(f"Crafted '{item_name}'.")
            return True
        else:
            print("Inventory is full. Cannot add the crafted item.")
            return False
