import os

structure = """
Game/
├── main.py
├── config.py
├── modules/
│   ├── camera.py
│   ├── world.py
│   ├── player.py
│   ├── weapon.py
│   ├── block.py
│   ├── animated_sprite.py
│   ├── inventory.py
│   ├── crafting.py
│   ├── items.py
│   ├── enemies.py
│   └── ui.py
├── assets/
│   ├── img/
│   │   ├── blocks/
│   │   │   ├── stone.png
│   │   │   ├── grass.png
│   │   │   ├── tree.png
│   │   │   ├── grass1.png
│   │   │   ├── block_5.png
│   │   │   ├── ARW2DSprite.png
│   │   │   └── player.png
│   │   ├── items/
│   │   │   ├── pickaxe.png
│   │   │   ├── sword.png
│   │   │   └── ... (other items)
│   │   ├── ui/
│   │   │   ├── inventory_slot.png
│   │   │   ├── health_bar.png
│   │   │   ├── health_foreground.png
│   │   │   └── ... (other UI elements)
│   │   └── enemies/
│   │       ├── zombie.png
│   │       ├── skeleton.png
│   │       └── ... (other enemies)
│   ├── maps/
│   │   └── map.txt
│   └── sounds/
│       ├── bg_music.mp3
│       ├── jump.wav
│       ├── mining.wav
│       └── ... (other sound effects)
├── data/
│   ├── items.json
│   ├── recipes.json
│   └── enemies.json
├── logs/
│   └── game.log
├── README.md
├── requirements.txt
└── LICENSE
"""

def create_structure(base_path, structure):
    for line in structure.splitlines():
        line = line.strip()
        if line.endswith('/'):
            os.makedirs(os.path.join(base_path, line[:-1]), exist_ok=True)
        elif line:
            os.makedirs(os.path.dirname(os.path.join(base_path, line)), exist_ok=True)
            open(os.path.join(base_path, line), 'a').close()

create_structure('.', structure)