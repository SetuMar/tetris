import pygame

GRID_SIZE = 25
GRID_COLOR = (255, 255, 255)
GRID_PADDING = 50

NUM_X_GRIDS = 10
NUM_Y_GRIDS = 20

GRID_WIDTH = NUM_X_GRIDS * GRID_SIZE + GRID_PADDING
GRID_HEIGHT = NUM_Y_GRIDS * GRID_SIZE + GRID_PADDING + 25

GRID_TOP = GRID_SIZE
GRID_LEFT = GRID_SIZE
GRID_RIGHT = GRID_LEFT + GRID_WIDTH - GRID_PADDING
GRID_BOTTOM = GRID_TOP + GRID_HEIGHT - (GRID_SIZE + GRID_PADDING)

FONT_SIZE = 20
FONT = pygame.font.Font('Roboto-Medium.ttf', FONT_SIZE)

# time in s between drops
TIME_BETWEEN_DROPS = 0.5
SOFT_DROP_TIME = 0.1

# SHOW DEBUG ITEMS (HIT BOXES)
DEBUG = False

# CONTROLS
MOVE_LEFT = pygame.K_LEFT
MOVE_RIGHT = pygame.K_RIGHT
ROTATE_RIGHT = pygame.K_UP
ROTATE_LEFT = pygame.K_z
SOFT_DROP = pygame.K_DOWN
HARD_DROP = pygame.K_SPACE
PAUSE = pygame.K_ESCAPE
HOLD_KEY = pygame.K_c