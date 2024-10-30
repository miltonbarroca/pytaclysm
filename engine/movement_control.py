from entities.entity import *
import tcod

class MovementControls:
    def __init__(self, player: Player, game_map, entities):
        self.player = player
        self.game_map = game_map
        self.entities = entities

    def handle_input(self, event):
        """Handles player movement input events"""
        # Movimentação para cima, baixo, esquerda e direita
        if event.sym == tcod.event.KeySym.w:  # Cima
            self.player.move(0, -1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.s:  # Baixo
            self.player.move(0, 1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.a:  # Esquerda
            self.player.move(-1, 0, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.d:  # Direita
            self.player.move(1, 0, self.game_map, self.entities)
        
        # Movimentação diagonal
        elif event.sym == tcod.event.KeySym.q:  # Cima Esquerda
            self.player.move(-1, -1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.e:  # Cima Direita
            self.player.move(1, -1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.z:  # Baixo Esquerda
            self.player.move(-1, 1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.c:  # Baixo Direita
            self.player.move(1, 1, self.game_map, self.entities)