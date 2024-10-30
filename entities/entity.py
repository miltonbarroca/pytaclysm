import random

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

class Player(Entity):
    def __init__(self, x, y, char='@', color=None, name='Player'):
        super().__init__(x, y, char, color, name, blocks=True)

class Cat(Entity):
    def __init__(self, x, y, char='C', color=None, name='Gato'):
        super().__init__(x, y, char, color, name, blocks=True)

    def get_random_move(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return random.choice(directions)