import tcod
import tileset.color as color
from engine.constants import SCREEN_WIDTH, SCREEN_HEIGHT, HUD

def render_hud(console: tcod.console.Console, player_health: int):
    """Renderiza informações do personagem no HUD."""
    hud_x_start = SCREEN_WIDTH - HUD  # Coloca a HUD no final da tela, após o mapa
    hud_width = HUD                   # Largura da HUD

    # Desenha um fundo preto para o HUD
    for y in range(SCREEN_HEIGHT):
        for x in range(hud_x_start, hud_x_start + hud_width):
            console.rgb[x, y] = (ord(" "), color.COLORS['black'], color.COLORS['black'])

    # Exibe informações do personagem (Vida)
    console.print(hud_x_start + 1, 1, f"Vida: {player_health}/100", fg=(255, 0, 0))

    # Exibe a barra de vida logo abaixo da informação de vida
    render_bar(console, x=hud_x_start + 1, y=2, width=30, current_value=player_health, max_value=100, 
               fg_color=(255, 0, 0), bg_color=(50, 50, 50))

def render_bar(console, x, y, width, current_value, max_value, fg_color, bg_color):
    """Renderiza uma barra horizontal para status como vida ou stamina."""
    bar_width = int((current_value / max_value) * width)  # Calcula o comprimento da barra baseado na vida
    console.draw_rect(x, y, width, 1, ord(" "), bg=bg_color)  # Desenha o fundo da barra
    if bar_width > 0:
        console.draw_rect(x, y, bar_width, 1, ord(" "), bg=fg_color)  # Desenha a barra preenchida
