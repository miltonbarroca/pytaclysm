from tileset.color import COLORS
import random

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.passable_tiles = {
            'forest_ground': True,
            'forest_ground_var': True,
            'dark_grass': True,
            'clearing': True,
            'bush': False,
            'tree': False,
            'tree_trunk': False,
            'cabin_wall': False,
            'cabin_floor': True,
            'river': False,
            'window': False,
            'door': True
        }

    def initialize_tiles(self):
        tiles = [['forest_ground' for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_forest(self):
        for x in range(self.width):
            for y in range(self.height):
                roll = random.random()
                if roll < 0.6:  
                    self.tiles[x][y] = 'forest_ground'
                elif roll < 0.7:
                    self.tiles[x][y] = 'forest_ground_var'
                elif roll < 0.8:
                    self.tiles[x][y] = 'dark_grass'
                elif roll < 0.9:
                    self.tiles[x][y] = 'clearing'
                elif roll < 0.95:
                    self.tiles[x][y] = 'bush'
                else:
                    if random.random() < 0.5:
                        self.tiles[x][y] = "tree"
                    else:
                        self.tiles[x][y] = "tree_trunk"

    def make_cabin(self, x, y, width, height):
        for x1 in range(x, x + width):
            for y1 in range(y, y + height):
                if x1 == x or x1 == x + width - 1 or y1 == y or y1 == y + height - 1:
                    self.tiles[x1][y1] = 'cabin_wall'
                else:
                    self.tiles[x1][y1] = 'cabin_floor'
        
        door_x = x + width // 2
        door_y = y + height - 1
        self.tiles[door_x][door_y] = 'door'

        window1_x, window1_y = x, y + height // 3
        window2_x, window2_y = x + width - 1, y + 2 * height // 3
        self.tiles[window1_x][window1_y] = 'window'
        self.tiles[window2_x][window2_y] = 'window'

    def make_river(self, start_x, start_y, length):
        x, y = start_x, start_y
        for _ in range(length):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[x][y] = 'river'
            direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            x += direction[0]
            y += direction[1]

    def is_blocked(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        tile_type = self.tiles[x][y]
        return not self.passable_tiles.get(tile_type, False)