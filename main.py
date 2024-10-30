import random
import tcod
from tcod import libtcodpy
import tileset.color as color
from entities.entity import Player
from entities.entity import Cat
from engine.movement_control import MovementControls
from map.game_map import GameMap

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45


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

class Engine:
    def __init__(self):
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        
        self.game_map.make_forest()
        self.game_map.make_river(10, 5, 30)
        self.game_map.make_cabin(20, 15, 10, 10)
        
        self.player = Player(25, 20, color=color.COLORS['player'])
        self.entities = [self.player]
        self.spawn_cats(1)
        
        self.movement_controls = MovementControls(self.player, self.game_map, self.entities)
        
        self.player_turn = True

    def spawn_cats(self, number):
        for _ in range(number):
            x = random.randint(20, 29)
            y = random.randint(15, 24)
            if not self.game_map.is_blocked(x, y):
                cat = Cat(x, y, color=color.COLORS['cat'])
                self.entities.append(cat)

    def render(self, console):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile = self.game_map.tiles[x][y]
                if tile == "tree":
                    console.print(x, y, 'o', bg=color.COLORS['tree'])
                elif tile == "forest_ground":
                    console.print(x, y, ' ', bg=color.COLORS['forest_ground'])
                elif tile == "forest_ground_var":
                    console.print(x, y, ' ', bg=color.COLORS['forest_ground_var'])
                elif tile == "dark_grass":
                    console.print(x, y, ' ', bg=color.COLORS['dark_grass'])
                elif tile == "clearing":
                    console.print(x, y, ' ', bg=color.COLORS['clearing'])
                elif tile == "bush":
                    console.print(x, y, '*', bg=color.COLORS['bush'])
                elif tile == 'cabin_floor':
                    console.print(x, y, ' ', bg=color.COLORS['cabin_floor'])
                elif tile == 'cabin_wall':
                    console.print(x, y, '#', bg=color.COLORS['cabin_wall'])
                elif tile == 'tree_trunk':
                    console.print(x, y, 'O', bg=color.COLORS['tree_trunk'])
                elif tile == "river":
                    console.print(x, y, '~', bg=color.COLORS['river'])
                elif tile == 'window':
                    console.print(x, y, '=', bg=color.COLORS['window'])
                elif tile == 'door':
                    console.print(x, y, '+', bg=color.COLORS['door'])
                else:
                    console.print(x, y, ' ', bg=color.COLORS['dark_wall'])

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

    def handle_input(self, event):
        if self.player_turn:
            self.movement_controls.handle_input(event)
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
        "tileset/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        tileset=tileset,
        title="Pytaclysm",
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