import pygame
from settings   import *
from engine     import *
from state_menu import *

pygame.mixer.init(44100, 16, 2, 1024)
pygame.init()


first_state            = "menu"
first_state_parameters = {}

states = {
        "menu": Menu([
            ("Resume"  , "game", {"new": False}),
            ("New game", "game", {"new": True}),
            ("Score"   , "score", {"total_score": 0, "edit": False}),
            ("Settings", [("fps", (False, True)), ("Music", (True, False))]),
            ("About"   , "about", {}),
            ("Exit game", Menu.MENU_QUIT)
            ])
        }
if __name__ == "__main__":
    try:
        game = Engine(
                states,
                first_state,
                first_state_parameters,
                screen_size,
                window_title="Little PyBall Game by Sharavsambuu")
        game.run()
    except Exception as ex:
        print(ex)
        pass
