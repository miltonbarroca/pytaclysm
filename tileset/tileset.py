import tcod
import tileset.color as color

def render(console, game_map, entities):
    # Renderizar o mapa
    for y in range(game_map.height):
        for x in range(game_map.width):
            tile = game_map.tiles[x][y]
            if tile == "tree":
                console.print(x, y, 'o', bg=color.COLORS['tree'])
            elif tile == "door":
                console.print(x, y, '+', bg=color.COLORS['door'])
            elif tile == "open_door":
                console.print(x, y, '/', bg=color.COLORS['open_door'])
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
            
            else:
                console.print(x, y, ' ', bg=color.COLORS['dark_wall'])

    # Renderizar as entidades
    for entity in entities:
        console.print(entity.x, entity.y, entity.char, fg=entity.color)
