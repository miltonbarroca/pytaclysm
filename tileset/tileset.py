import json
import tcod
import tileset.color as color

# Carregar dados dos tiles do JSON
with open('data/tiles.json', 'r', encoding='utf-8') as file:
    tiles_data = json.load(file)

def render(console, game_map, entities):
    # Renderizar o mapa
    for y in range(game_map.height):
        for x in range(game_map.width):
            tile = game_map.tiles[x][y]
            if tile in tiles_data:
                tile_info = tiles_data[tile]
                char = tile_info.get("char", " ")
                tile_color = color.COLORS.get(tile_info["color"], color.COLORS["dark_wall"])
                console.print(x, y, char, bg=tile_color)
            else:
                console.print(x, y, ' ', bg=color.COLORS["dark_wall"])

    # Renderizar as entidades
    for entity in entities:
        console.print(entity.x, entity.y, entity.char, fg=entity.color)
