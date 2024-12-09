from entities.entity import Entity
from engine.interactions import handle_interaction

class Player(Entity):
    def __init__(self, x, y, char='@', color=None, name='Player'):
        super().__init__(x, y, char, color, name, blocks=True)
        self.interactions = {}

    def set_interactions(self, interactions):
        self.interactions = interactions

    def interact(self, dx, dy, game_map):
        handle_interaction(self, dx, dy, game_map)
