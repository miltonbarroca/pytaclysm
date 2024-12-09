import random
import tcod
import json
import tileset.color as color
from entities.player import Player
from entities.entity import Cat
from engine.controls import MovementControls
from map.game_map import GameMap
from engine.constants import *
from tileset.tileset import render

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
        
        with open("data/tiles.json") as f:
            self.interactions = json.load(f)
        
        self.player.set_interactions(self.interactions)
        
        self.player_turn = True

        # Atributos para o HUD
        self.player_health = 100  # Vida do jogador
        self.player_stamina = 50  # Stamina do jogador

    def spawn_cats(self, number):
        for _ in range(number):
            x = random.randint(20, 29)
            y = random.randint(15, 24)
            if not self.game_map.is_blocked(x, y):
                cat = Cat(x, y, color=color.COLORS['cat'])
                self.entities.append(cat)

    def handle_input(self, event):
        if self.player_turn:
            self.movement_controls.handle_input(event)
            self.end_player_turn()

    def end_player_turn(self):
        self.player_turn = False
        self.enemy_turn()

    def enemy_turn(self):
        for entity in self.entities:
            if isinstance(entity, Cat):
                dx, dy = entity.get_random_move()
                entity.move(dx, dy, self.game_map, self.entities)
        self.player_turn = True

    def render(self, console):
        # Renderiza o mapa e as entidades
        render(console, self.game_map, self.entities)
        
        # Renderiza o HUD
        self.render_hud(console)

    def render_hud(self, console: tcod.console.Console):
        """Renderiza informações do personagem no HUD."""
        hud_x_start = SCREEN_WIDTH  # O HUD começa logo após a área do mapa
        hud_width = HUD             # Largura da HUD

        # Desenha um fundo preto para o HUD
        for y in range(SCREEN_HEIGHT):
            for x in range(hud_x_start, hud_x_start + hud_width):
                console.rgb[x, y] = (ord(" "), color.COLORS['black'], color.COLORS['black'])

        # Exibe informações do personagem
        console.print(hud_x_start + 1, 1, f"Vida: {self.player_health}/100", fg=(255, 0, 0))
        console.print(hud_x_start + 1, 4, "Pressione H para abrir o inventário.", fg=(255, 255, 255))

        # Exemplo de barra de vida
        self.render_bar(
            console, x=20, y=1, width=30,
            current_value=self.player_health, max_value=100,
            fg_color=(255, 0, 0), bg_color=(50, 50, 50)
        )

    def render_bar(self, console, x, y, width, current_value, max_value, fg_color, bg_color):
        """Renderiza uma barra horizontal para status como vida ou stamina."""
        bar_width = int((current_value / max_value) * width)
        console.draw_rect(x, y, width, 1, ord(" "), bg=bg_color)
        if bar_width > 0:
            console.draw_rect(x, y, bar_width, 1, ord(" "), bg=fg_color)
