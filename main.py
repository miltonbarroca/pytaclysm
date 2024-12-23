import tcod
from engine.engine import Engine
from engine.constants import *

def main():
    tileset = tcod.tileset.load_tilesheet(
        "tileset/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    # Ajustamos a largura total para incluir a HUD na direita
    with tcod.context.new_terminal(
        SCREEN_WIDTH + HUD,
        SCREEN_HEIGHT,  
        tileset=tileset,
        title="Pytaclysm",
        vsync=True,
    ) as context:
        console = tcod.console.Console(SCREEN_WIDTH + HUD, SCREEN_HEIGHT, order="F")
        engine = Engine()
        
        while True:
            engine.render(console)  # Renderizamos o mapa e a HUD
            context.present(console)
            
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                elif event.type == "KEYDOWN":
                    engine.handle_input(event)

if __name__ == "__main__":
    main()
