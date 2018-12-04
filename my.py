import pygame, file

""" GAME """
VERSION = "1.0 dev build"
ENGINE = None

CONFIG = file.File("config", {
	'screen_width': 900,
	'screen_height': 600,
	'windowed': True,
	'fps': 60,
	'muted': False,
	'hardware_accelerated': False})

PLATFORM_WIDTH = 5
PLATFORM_HEIGHT = 5

SCREEN_WIDTH = CONFIG.get('screen_width')
SCREEN_HEIGHT = CONFIG.get('screen_height')
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

SCREEN_HALF_WIDTH = SCREEN_WIDTH / 2
SCREEN_HALF_HEIGHT = SCREEN_HEIGHT / 2
SCREEN_HALF_SIZE = (SCREEN_HALF_WIDTH, SCREEN_HALF_HEIGHT)

WINDOWED = CONFIG.get("windowed")
FPS = CONFIG.get('fps')
MUTED = CONFIG.get("muted")
HARDWARE_ACCELERATED = CONFIG.get('hardware_accelerated')

BLOCK_NONE = 0
BLOCK_DIRT = 1
BLOCK_ROCK = 2
BLOCK_GRASS = 3
BLOCK_COLORS = {
	BLOCK_NONE: (0, 0, 0, 0),
	BLOCK_DIRT: (117, 76, 16, 255),
	BLOCK_ROCK: (141, 155, 141, 255),
	BLOCK_GRASS: (48, 219, 48, 255)
}

""" PHYSICS"""
GRAVITY = pygame.Vector2((0, 0.3))

""" FONTS """
pygame.font.init()


def FONT(size, bold=False, italic=False, underline=False):
	font = pygame.font.Font("assets/fonts/Kenney Future Narrow.ttf", size)
	font.set_bold(bold)
	font.set_italic(italic)
	font.set_underline(underline)
	return font


def FONT_HIGH(size, bold=False, italic=False, underline=False):
	font = pygame.font.Font("assets/fonts/Kenney Future.ttf", size)
	font.set_bold(bold)
	font.set_italic(italic)
	font.set_underline(underline)
	return font


NAMES = ["Stalin", "Lenin", "Mussolini", "Hitler", "Trump", "Bolsonaro", "Lula",
		 "Mansilha", "Coelho"]

""" COLORS """
BLACK = (52, 73, 94)
WHITE = (236, 240, 241)
BLUE = (41, 128, 185)
LIGHT_BLUE = (52, 152, 219)
RED = (244, 67, 54)
GREEN = (46, 204, 113)
DARK_GREEN = (39, 174, 96)
ORANGE = (243, 156, 18)
GREY = (127, 140, 141)
LIGHT_GREY = (149, 165, 166)
PINK = (155, 89, 182)
YELLOW = (241, 196, 15)

# https://flatuicolors.com/
# https://flatuicolors.com/palette/defo
