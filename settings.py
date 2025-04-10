import pygame
import os 

TILE_SIZE     = 32  
TILE_DIM      = (16, 16)  
EXTRA_WIDTH   = 5 * TILE_SIZE 
SCREEN_WIDTH  = TILE_DIM[0] * TILE_SIZE + EXTRA_WIDTH
SCREEN_HEIGHT = TILE_DIM[1] * TILE_SIZE
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)

PPM = float(TILE_SIZE) 
MPP = 1.0 / PPM        

GAME_GRAVITY        = (0.0, -15.0) 
DEATH_STATE_GRAVITY = (0.0,  25.0) 

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255) 
YELLOW = (255, 255, 0) 

K_MOVE_LEFT  = pygame.K_LEFT      
K_MOVE_RIGHT = pygame.K_RIGHT     
K_JUMP       = pygame.K_z         
K_ACTION     = pygame.K_x        
K_SHOOT      = pygame.K_UP          
K_PAUSE_QUIT = pygame.K_ESCAPE
K_RETURN     = pygame.K_RETURN
K_BACKSPACE  = pygame.K_BACKSPACE

WINDOW_TITLE = "Little PyBall Game by Sharavsambuu.G"

FONT_PATH       = os.path.join("data", "font", "fsex2p00_public.ttf")
SCORE_FILE_PATH = os.path.join("data", "score", "score.txt")

SOUND_MUSIC_GAME  = os.path.join("data", "sound", "music", "DikkiPainguinLoop(rev-1).ogg")
SOUND_MUSIC_ABOUT = os.path.join("data", "sound", "music", "song12.ogg")
SOUND_FX_POP      = os.path.join("data", "sound", "fx", "ploop.wav")
SOUND_FX_THUMP    = os.path.join("data", "sound", "fx", "thump.ogg")
SOUND_FX_COMBO    = os.path.join("data", "sound", "fx", "boom.ogg")
