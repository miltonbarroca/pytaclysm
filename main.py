import random
import tcod
from tcod import libtcodpy

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

COLORS = {
    'dark_wall': libtcodpy.Color(20, 20, 40),
    'forest_ground': libtcodpy.Color(34, 139, 34),  
    'forest_ground_var': libtcodpy.Color(60, 100, 40),
    'dark_grass': libtcodpy.Color(20, 70, 20),
    'clearing': libtcodpy.Color(85, 107, 47),
    'bush': libtcodpy.Color(34, 139, 84),
    'cabin_floor': libtcodpy.Color(139, 69, 19),
    'cabin_wall': libtcodpy.Color(139, 69, 19),
    'tree': libtcodpy.Color(123, 63, 0),
    'tree_trunk': libtcodpy.Color(101, 67, 33),
    'river': libtcodpy.Color(0, 0, 255),
    'player': libtcodpy.Color(255, 255, 255),
    'cat': libtcodpy.Color(200, 100, 100),
}

class Entity:
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy, game_map, entities):
        if not game_map.is_blocked(self.x + dx, self.y + dy) and not self.is_blocked(entities, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def is_blocked(self, entities, x, y):
        for entity in entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return True
        return False

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

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
                if 0 <= x1 < self.width and 0 <= y1 < self.height:
                    if x1 == x or x1 == x + width - 1 or y1 == y or y1 == y + height - 1:
                        self.tiles[x1][y1] = 'cabin_wall'
                    else:
                        self.tiles[x1][y1] = 'cabin_floor'

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
        return self.tiles[x][y] in ["tree", "tree_trunk", "cabin_wall", "bush", "river"]

class Engine:
    def __init__(self):
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        
        self.game_map.make_forest()
        self.game_map.make_river(10, 5, 30)
        self.game_map.make_cabin(20, 15, 10, 10)
        
        self.player = Entity(25, 20, '@', COLORS['player'], 'Jogador', blocks=True)
        self.entities = [self.player]
        self.spawn_cats(3)
        
        self.player_turn = True

    def spawn_cats(self, number):
        for _ in range(number):
            x = random.randint(20, 29)
            y = random.randint(15, 24)
            if not self.game_map.is_blocked(x, y):
                cat = Entity(x, y, 'C', COLORS['cat'], 'Gato', blocks=True)
                self.entities.append(cat)

    def render(self, console):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile = self.game_map.tiles[x][y]
                if tile == "tree":
                    console.print(x, y, 'o', bg=COLORS['tree'])
                elif tile == "forest_ground":
                    console.print(x, y, ' ', bg=COLORS['forest_ground'])
                elif tile == "forest_ground_var":
                    console.print(x, y, ' ', bg=COLORS['forest_ground_var'])
                elif tile == "dark_grass":
                    console.print(x, y, ' ', bg=COLORS['dark_grass'])
                elif tile == "clearing":
                    console.print(x, y, ' ', bg=COLORS['clearing'])
                elif tile == "bush":
                    console.print(x, y, '*', bg=COLORS['bush'])
                elif tile == 'cabin_floor':
                    console.print(x, y, ' ', bg=COLORS['cabin_floor'])
                elif tile == 'cabin_wall':
                    console.print(x, y, '#', bg=COLORS['cabin_wall'])
                elif tile == 'tree_trunk':
                    console.print(x, y, 'O', bg=COLORS['tree_trunk'])
                elif tile == "river":
                    console.print(x, y, '~', bg=COLORS['river'])
                else:
                    console.print(x, y, ' ', bg=COLORS['dark_wall'])

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

    def handle_input(self, event):
        if self.player_turn:
            if event.sym == tcod.event.KeySym.UP:
                self.player.move(0, -1, self.game_map, self.entities)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.DOWN:
                self.player.move(0, 1, self.game_map, self.entities)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.LEFT:
                self.player.move(-1, 0, self.game_map, self.entities)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.RIGHT:
                self.player.move(1, 0, self.game_map, self.entities)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.PERIOD:
                self.end_player_turn()

    def end_player_turn(self):
        self.player_turn = False
        self.enemy_turn()

    def enemy_turn(self):
        for entity in self.entities:
            if entity.name == 'Gato':
                dx, dy = self.random_move()
                entity.move(dx, dy, self.game_map, self.entities)
        self.player_turn = True

    def random_move(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return random.choice(directions)

def main():
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        tileset=tileset,
        title="Roguelike - Floresta com Cabana e Rios",
        vsync=True,
    ) as context:
        console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        engine = Engine()
        
        while True:
            engine.render(console)
            context.present(console)
            
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                elif event.type == "KEYDOWN":
                    engine.handle_input(event)

if __name__ == "__main__":
    main()