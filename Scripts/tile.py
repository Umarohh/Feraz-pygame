import pygame
from Scripts.camera import Camera

TILE_SIZE = 32  # Set a constant tile size
TILE_IMAGES = {}

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()

        self.tile_type = tile_type
        self.image = TILE_IMAGES.get(tile_type)
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))

    @staticmethod
    def load_tile_images():
        global TILE_IMAGES
        TILE_IMAGES = {
            1: pygame.image.load('Assets/Universal/Tiles/grass.png').convert_alpha(),
            2: pygame.image.load('Assets/Universal/Tiles/dirt.png').convert_alpha(),
            3: pygame.image.load('Assets/Universal/Tiles/concrete1.png').convert_alpha(),
            4: pygame.image.load('Assets/Universal/Tiles/concrete2.png').convert_alpha(),
            5: pygame.image.load('Assets/Universal/Tiles/concrete3.png').convert_alpha(),
            6: pygame.image.load('Assets/Universal/Tiles/cobble.png').convert_alpha(),

            # Add more tile types as needed
        }

    def update(self):
        # Optional: Add animation, effects, or tile-specific logic
        pass

class Tilemap:
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.map_data = []  # Initialize map_data as an empty list
        self.pixel_width = 0
        self.pixel_height = 0
    
    def _parse_file(self, file_path):
        """Read the file and return map data as a 2D array."""
        map_data = []
        with open(file_path, 'r') as file:
            for line in file:
                # Convert each line to a list of integers, where each represents a tile
                map_data.append([int(x) for x in line.strip().split()])
        return map_data
    

    def create_tiles(self, map_data):
        """Create tiles based on 2D map data."""
        for y, row in enumerate(map_data):
            for x, tile_type in enumerate(row):
                # Only create a tile if the tile_type is valid (i.e., exists in TILE_IMAGES)
                if tile_type in TILE_IMAGES:
                    tile = Tile(x, y, tile_type)
                    self.tiles.add(tile)
        
        map_width = max((len(row) for row in map_data), default=0)
        self.pixel_width = map_width * TILE_SIZE
        self.pixel_height = len(map_data) * TILE_SIZE

    def load_from_file(self, file_path):
        """Load the tilemap from a text file."""
        self.tiles.empty()  # Clear any existing tiles
        map_data = self._parse_file(file_path)
        self.create_tiles(map_data)  # Create tiles based on parsed data
        
    def update(self):
        """Update all tiles."""
        self.tiles.update()

    def render(self, screen, camera):
        """Render the tilemap."""
        visible_area = screen.get_rect().move(camera.camera.topleft)
        for tile in self.tiles:
            if tile.rect.colliderect(visible_area):
                screen.blit(tile.image, camera.apply(tile))
