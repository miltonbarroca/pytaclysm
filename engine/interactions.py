def toggle_door(game_map, target_x, target_y, interaction):
    """Alterna o estado de uma porta."""
    if interaction["state"] == "closed":
        # Abrir a porta
        game_map.tiles[target_x][target_y] = 'open_door'
        interaction["state"] = "open"
        interaction["is_passable"] = True
        print("A porta se abre.")
    elif interaction["state"] == "open":
        # Fechar a porta
        game_map.tiles[target_x][target_y] = 'door'
        interaction["state"] = "closed"
        interaction["is_passable"] = False
        print("Voce fechou a porta.")

def handle_interaction(player, dx, dy, game_map):
    """Gerencia a interação do jogador com o ambiente."""
    # Verifica o tile na direção indicada
    target_x, target_y = player.x + dx, player.y + dy
    if 0 <= target_x < game_map.width and 0 <= target_y < game_map.height:
        tile = game_map.tiles[target_x][target_y]

        # Busca a interação no dicionário de interações
        if tile in player.interactions:
            interaction = player.interactions[tile]
            print(interaction["message"])

            # Gerencia ações específicas
            action = interaction.get("action")
            if action == "toggle_door":
                toggle_door(game_map, target_x, target_y, interaction)
            elif action == "look_out":
                print("E uma bela paisagem...")
        else:
            print("Nao ha nada para interagir nessa direcao.")
