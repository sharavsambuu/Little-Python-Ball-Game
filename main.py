import pygame

pygame.mixer.init(44100, 16, 2, 1024)
pygame.init()

if __name__ == "__main__":
    try:
        game = Engine(
                states,
                first_state,
                first_state_parameters,
                screen_size,
                window_title="Little PyBall Game by Sharavsambuu")
        game.run()
    except:
        pass
