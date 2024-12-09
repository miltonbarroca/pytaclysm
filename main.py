import tcod
from engine.engine import Engine
from engine.constants import *

def main():
    tileset = tcod.tileset.load_tilesheet(
        "tileset/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    # O terminal é inicializado com NEW_HEIGHT para incluir a área do HUD
    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        NEW_HEIGHT,  # Use NEW_HEIGHT para incluir o HUD
        tileset=tileset,
        title="Pytaclysm",
        vsync=True,
    ) as context:
        # O console também precisa refletir a altura do HUD
        console = tcod.console.Console(SCREEN_WIDTH, NEW_HEIGHT, order="F")
        engine = Engine()
        
        while True:
            engine.render(console)  # Renderiza o jogo e o HUD
            context.present(console)
            
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                elif event.type == "KEYDOWN":
                    engine.handle_input(event)

if __name__ == "__main__":
    main()
