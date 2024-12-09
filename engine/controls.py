from entities.player import Player
import tcod

class MovementControls:
    def __init__(self, player: Player, game_map, entities):
        self.player = player
        self.game_map = game_map
        self.entities = entities
        self.interact_mode = False

    def handle_input(self, event):
        """Handles player movement input events and interaction"""
        if event.sym == tcod.event.KeySym.f:
            # Ativa o modo de interação
            self.interact_mode = True
            print("Modo de interação ativado. Pressione uma direção para interagir.")
            return

        if self.interact_mode:
            # Se estamos no modo de interação, a próxima tecla de movimento será uma interação
            dx, dy = 0, 0
            if event.sym == tcod.event.KeySym.w:
                dx, dy = 0, -1
            elif event.sym == tcod.event.KeySym.s:
                dx, dy = 0, 1
            elif event.sym == tcod.event.KeySym.a:
                dx, dy = -1, 0
            elif event.sym == tcod.event.KeySym.d:
                dx, dy = 1, 0
            elif event.sym == tcod.event.KeySym.q:
                dx, dy = -1, -1
            elif event.sym == tcod.event.KeySym.e:
                dx, dy = 1, -1
            elif event.sym == tcod.event.KeySym.z:
                dx, dy = -1, 1
            elif event.sym == tcod.event.KeySym.c:
                dx, dy = 1, 1

            if dx != 0 or dy != 0:
                # Realiza a interação na direção especificada
                self.player.interact(dx, dy, self.game_map)
                self.interact_mode = False  # Desativa o modo de interação após a ação
                return

        # Caso contrário, é um movimento normal
        if event.sym == tcod.event.KeySym.w:
            self.player.move(0, -1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.s:
            self.player.move(0, 1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.a:
            self.player.move(-1, 0, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.d:
            self.player.move(1, 0, self.game_map, self.entities)
        
        # Movimentação diagonal
        elif event.sym == tcod.event.KeySym.q:
            self.player.move(-1, -1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.e:
            self.player.move(1, -1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.z:
            self.player.move(-1, 1, self.game_map, self.entities)
        elif event.sym == tcod.event.KeySym.c:
            self.player.move(1, 1, self.game_map, self.entities)
