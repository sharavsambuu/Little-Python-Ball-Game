import pygame
import sys
import os
import traceback 

try:
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.mixer.pre_init(44100, -16, 2, 512) 
    pygame.mixer.init()
    pygame.init() 
    print(f"Pygame {pygame.version.ver} (SDL {pygame.version.SDL}) Initialized")
except pygame.error as e:
    print(f"Error initializing Pygame: {e}")
    sys.exit(1)

from settings    import SCREEN_SIZE, WINDOW_TITLE
from engine      import Engine
from state       import State 
from state_menu  import Menu
from state_about import About
from state_game  import Game
from state_death import Death
from state_score import Score
from state_win   import Win


def main():
    print("Setting up game...")
    print("Creating game states...")
    menu_structure = [
        ["Resume"   , "game" , {"new" : False}],
        ["New game" , "game" , {"new" : True }],
        ["Score"    , "score", {"edit": False}],
        ["Settings" , [ 
            ["Music", (True, False)],
        ]],
        ["About"    , "about", {}],
        ["Exit game", Menu.MENU_QUIT]
    ]

    states = {
        "menu"  : Menu(menu_structure),
        "about" : About(),
        "game"  : Game(),
        "death" : Death(),
        "score" : Score(),
        "win"   : Win()
    }
    print("States created.") 

    first_state_key    = "menu"
    first_state_params = {}

    game_engine = None 
    try:
        print("Initializing game engine...")
        game_engine = Engine(
            states             = states, 
            first_state_key    = first_state_key,
            first_state_params = first_state_params,
            window_title       = WINDOW_TITLE
        )
        print("Engine initialized and initial state entered.")

        print("Starting game loop...")
        game_engine.run()
    except Exception as ex:
        print("\n--- An unhandled error occurred during game execution! ---")
        print(f"Error Type: {type(ex).__name__}")
        print(f"Error Details: {ex}")
        traceback.print_exc() 
        print("-------------------------------------------------------")

    finally:
        pygame.quit()
        print("Pygame quit.")
        print("Game exited.")

if __name__ == "__main__":
    main()