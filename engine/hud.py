import tcod
import tileset.color as color
from engine.constants import SCREEN_WIDTH, SCREEN_HEIGHT, HUD

def render_hud(console: tcod.console.Console, player_health: int):
    """Renderiza informações do personagem no HUD."""
    hud_x_start = SCREEN_WIDTH  # O HUD começa logo após a área do mapa
    hud_width = HUD             # Largura da HUD

    # Desenha um fundo preto para o HUD
    for y in range(SCREEN_HEIGHT):
        for x in range(hud_x_start, hud_x_start + hud_width):
            console.rgb[x, y] = (ord(" "), color.COLORS['black'], color.COLORS['black'])

    # Exibe informações do personagem
    console.print(hud_x_start + 1, 1, f"Vida: {player_health}/100", fg=(255, 0, 0))
    console.print(hud_x_start + 1, 4, "Pressione H para abrir o inventário.", fg=(255, 255, 255))

    # Exemplo de barra de vida
    render_bar(
        console, x=20, y=1, width=30,
        current_value=player_health, max_value=100,
        fg_color=(255, 0, 0), bg_color=(50, 50, 50)
    )

def render_bar(console, x, y, width, current_value, max_value, fg_color, bg_color):
    """Renderiza uma barra horizontal para status como vida ou stamina."""
    bar_width = int((current_value / max_value) * width)
    console.draw_rect(x, y, width, 1, ord(" "), bg=bg_color)
    if bar_width > 0:
        console.draw_rect(x, y, bar_width, 1, ord(" "), bg=fg_color)
