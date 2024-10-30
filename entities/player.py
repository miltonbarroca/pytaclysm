from entities.entity import Entity

class Player(Entity):
    def __init__(self, x, y, char='@', color=None, name='Player'):
        super().__init__(x, y, char, color, name, blocks=True)
        self.interactions = {}

    def set_interactions(self, interactions):
        self.interactions = interactions

    def interact(self, dx, dy, game_map):
        # Verifica o tile na direção indicada
        target_x, target_y = self.x + dx, self.y + dy
        if 0 <= target_x < game_map.width and 0 <= target_y < game_map.height:
            tile = game_map.tiles[target_x][target_y]
            
            # Busca a interação no dicionário de interações
            if tile in self.interactions:
                interaction = self.interactions[tile]
                print(interaction["message"])
                
                #alternar o estado da porta
                if interaction.get("action") == "toggle_door":
                    if interaction.get("state") == "closed":
                        # Muda o estado da porta
                        game_map.tiles[target_x][target_y] = 'open_door'
                        interaction["state"] = "open"
                        interaction["is_passable"] = True
                        print("A porta se abre.")
                    else:
                        # Muda o estado da porta para "closed" e a torna não passável
                        game_map.tiles[target_x][target_y] = 'door'
                        interaction["state"] = "closed"
                        interaction["is_passable"] = False
                        print("Você fechou a porta.")
                
                elif interaction.get("action") == "look_out":
                    print("É uma bela paisagem...")
            else:
                print("Não há nada para interagir nessa direção.")
