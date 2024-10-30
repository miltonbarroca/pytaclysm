# engine.py

import tcod
from entities.player import Player
from map.game_map import GameMap
from tileset import color

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

class Engine:
    def __init__(self):
        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        self.game_map.make_forest()
        self.game_map.make_river(10, 5, 30)
        self.game_map.make_cabin(20, 15, 10, 10)
        
        self.player = Player(25, 20, '@', color.COLORS['player'], 'Jogador')
        self.entities = [self.player]

        self.player_turn = True

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
                elif tile == "river":
                    console.print(x, y, '~', bg=color.COLORS['river'])
                
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

    def handle_input(self, event):
        if self.player_turn:
            move_directions = {
                tcod.event.KeySym.UP: (0, -1), tcod.event.KeySym.DOWN: (0, 1),
                tcod.event.KeySym.LEFT: (-1, 0), tcod.event.KeySym.RIGHT: (1, 0),
                tcod.event.KeySym.q: (-1, -1), tcod.event.KeySym.e: (1, -1),
                tcod.event.KeySym.z: (-1, 1), tcod.event.KeySym.c: (1, 1)
            }
            if event.sym in move_directions:
                direction = move_directions[event.sym]
                self.player.handle_movement(direction, self.game_map, self.entities)
                self.player_turn = False

def main():
    tileset = tcod.tileset.load_tilesheet("tileset/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    
    with tcod.context.new_terminal(SCREEN_WIDTH, SCREEN_HEIGHT, tileset=tileset, title="Pytaclysm", vsync=True) as context:
        console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        engine = Engine()
        
        while True:
            console.clear()
            engine.render(console)
            context.present(console)
            
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                elif event.type == "KEYDOWN":
                    engine.handle_input(event)

if __name__ == "__main__":
    main()
