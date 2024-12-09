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
from engine.hud import render_hud  # Importa a função render_hud

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
        render_hud(console, self.player_health)  # Passa a vida do jogador para o HUD
