
# Game Title

**Short Description:**  
This is an isometric 2.5D exploration and adventure game where you control a character moving through layered terrain, gathering resources, and interacting with various elements in a lively isometric world.

##  World:

In this crimson-hued realm of ruin and redemption, you stand as the last scion of a forgotten royal bloodline. The Empire—once a beacon of power—now teeters on the edge of oblivion, besieged by twisted creatures bearing glowing relics of an ancient, evil god. Across sprawling isometric battlefields, you will discover and master the mysterious segis and arches, unlocking new strengths and long-dormant sorceries. From sun-scorched deserts to crumbling fortress-cities, a world stained in shades of red invites you to defy the cult that seeks to resurrect the shattered deity, even as you grapple with your own destiny. Will you safeguard the Empire’s future or dare to break the cycle of chaos forever? The choice—and the fate of this dying land—lies in your hands.

## Features

- **Isometric World:**  
  Experience a rich environment composed of multiple terrain layers, allowing you to move not only horizontally and vertically, but also adjust your character’s position across layered blocks.

- **Dynamic Character Controls:**  
  Move freely using the WASD keys, jump up layers with the Spacebar, and descend layers with the Left Shift key. This layered movement adds depth and complexity to the standard 2D navigation.

- **Animated Tiles and Characters:**  
  Enjoy smooth animations for certain blocks (like waterfalls or special tiles) and for your character. The world feels more alive as animated sprites cycle through frames, adding visual interest.

- **Resource Gathering and Crafting (Planned):**  
  Collect resources from the environment and craft them into tools, weapons, and other helpful items. Future updates aim to introduce a deeper crafting system and expanded inventory management.

- **Enemies and Combat (Planned):**  
  Defend yourself against enemies inhabiting various layers of the map. Engage in combat with basic weapons to protect your resources and explore safely.

## Controls

- **Move:** W, A, S, D  
- **Jump Up a Layer:** Spacebar  
- **Move Down a Layer:** Left Shift  
- **Quit Game:** Close the window or press the appropriate quit shortcut (e.g., Alt+F4 on Windows)

## Getting Started

1. **Install Dependencies:**  
   Ensure `pygame` is installed. You can install it via:  
   ```bash
   pip install pygame
   ```

2. **Run the Game:**  
   From the `Game/` directory, run:  
   ```bash
   python main.py
   ```

3. **Explore and Interact:**  
   Move your character around, explore the map, and experiment with changing layers.

## File Structure

- **main.py**: The entry point of the game.  
- **config.py**: Contains game-wide configuration constants.  
- **modules/**: Contains modularized code for camera, world, player, and other systems.  
- **assets/**: Holds images, maps, and sound files used by the game.  
- **data/**: Contains game data such as items, recipes, and enemy definitions.  
- **logs/**: Stores game logs.

## Future Plans

- Expanded crafting system and item variety.  
- Additional enemies with distinct behaviors.  
- Improved UI and inventory screens.  
- Sound effects and background music integration.

## Contributing

If you wish to contribute, please visit [Pygame’s contribution guidelines](https://www.pygame.org/contribute.html) to learn more about contributing to the ecosystem. We welcome bug reports, feature suggestions, and pull requests!
