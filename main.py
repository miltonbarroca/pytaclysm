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
    'cabin_floor': libtcodpy.Color(139, 69, 19),
    'cabin_wall': libtcodpy.Color(139, 69, 19),
    'tree': libtcodpy.Color(123, 63, 0),
    'tree_trunk': libtcodpy.Color(101, 67, 33),
    'player': libtcodpy.Color(255, 255, 255),
    'zombie': libtcodpy.Color(0, 255, 0),
}

class Entity:
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy, game_map):
        if not game_map.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

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
                if random.random() < 0.8:  
                    if random.random() < 0.3:
                        self.tiles[x][y] = 'forest_ground_var'
                    else:
                        self.tiles[x][y] = 'forest_ground'
                elif random.random() < 0.2:
                    if random.random() < 0.5:
                        self.tiles[x][y] = "tree"
                    else:
                        self.tiles[x][y] = "tree_trunk" 

    def make_cabin(self, x, y, width, height):
        # Paredes externas da cabana
        for x1 in range(x, x + width):
            for y1 in range(y, y + height):
                if 0 <= x1 < self.width and 0 <= y1 < self.height:
                    if x1 == x or x1 == x + width - 1 or y1 == y or y1 == y + height - 1:
                        # Espaço para a porta
                        if y1 == y + height // 2 and x <= x1 < x + 2:
                            self.tiles[x1][y1] = 'cabin_floor'  # Porta de 2 tiles
                        # Janelas nas paredes
                        elif (x1 == x + width // 2 or x1 == x + width // 2 + 1) and (y1 == y or y1 == y + height - 1):
                            self.tiles[x1][y1] = 'cabin_floor'  # Janelas na parede da frente e de trás
                        else:
                            self.tiles[x1][y1] = 'cabin_wall'
                    else:
                        # Interior da cabana
                        self.tiles[x1][y1] = 'cabin_floor'

    def is_blocked(self, x, y):
        # Verifica limites do mapa e se o tile é bloqueado
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        # Adiciona cabin_wall como bloqueio, além de tree e tree_trunk
        return self.tiles[x][y] in ["tree", "tree_trunk", "cabin_wall"]

class Engine:
    def __init__(self):
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        
        self.game_map.make_forest()
        self.game_map.make_cabin(20, 15, 10, 10)
        
        # Colocando o jogador no centro da cabana
        self.player = Entity(25, 20, '@', COLORS['player'], 'Jogador', blocks=True)
        
        self.entities = [self.player]
        self.spawn_zombies(3)
        
        self.player_turn = True

    def spawn_zombies(self, number):
        for _ in range(number):
            x = random.randint(20, 29)
            y = random.randint(15, 24)
            if not self.game_map.is_blocked(x, y):
                zombie = Entity(x, y, 'Z', COLORS['zombie'], 'Zumbi', blocks=True)
                self.entities.append(zombie)

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
                elif tile == 'cabin_floor':
                    console.print(x, y, ' ', bg=COLORS['cabin_floor'])
                elif tile == 'cabin_wall':
                    console.print(x, y, '#', bg=COLORS['cabin_wall'])
                elif tile == 'tree_trunk':
                    console.print(x, y, 'O', bg=COLORS['tree_trunk'])
                else:
                    console.print(x, y, ' ', bg=COLORS['dark_wall'])

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

    def handle_input(self, event):
        if self.player_turn:
            if event.sym == tcod.event.KeySym.UP:
                self.player.move(0, -1, self.game_map)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.DOWN:
                self.player.move(0, 1, self.game_map)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.LEFT:
                self.player.move(-1, 0, self.game_map)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.RIGHT:
                self.player.move(1, 0, self.game_map)
                self.end_player_turn()
            elif event.sym == tcod.event.KeySym.PERIOD:
                self.end_player_turn()

    def end_player_turn(self):
        self.player_turn = False
        self.enemy_turn()

    def enemy_turn(self):
        for entity in self.entities:
            if entity.name == 'Zumbi':
                dx, dy = self.random_move()
                entity.move(dx, dy, self.game_map)
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
        title="Roguelike - Cabana e Floresta",
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
                    if engine.player_turn:
                        engine.handle_input(event)

if __name__ == '__main__':
    main()
