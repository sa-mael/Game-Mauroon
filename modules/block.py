# modules/block.py

#class Block:
#    def __init__(self, block_id, name, image_path, is_solid=True, mining_level=1):
#        """
#        Initializes a block type.
#
#        :param block_id: Unique identifier for the block.
#        :param name: Name of the block.
#        :param image_path: Path to the block's image.
#        :param is_solid: Whether the block is solid (player cannot pass through).
#        :param mining_level: The level required to mine the block.
#        """
#        self.block_id = block_id
#        self.name = name
#        self.is_solid = is_solid
#        self.mining_level = mining_level
#
#        try:
#            self.image = pygame.image.load(image_path).convert_alpha()
#            self.image = pygame.transform.scale(self.image, (40, 40))
#        except pygame.error as e:
#            print(f"Error loading block image '{image_path}': {e}")
#            sys.exit()
