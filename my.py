import pygame, file

""" GAME """
ENGINE = None
LOGO = None

CONFIG = file.File("config", {
	'screen_width': 900,
	'screen_height': 600,
	'windowed': True,
	'fps': 30,
	'muted': False})

PLATFORM_WIDTH = 5
PLATFORM_HEIGHT = 5

SCREEN_WIDTH = CONFIG.get('screen_width')
SCREEN_HEIGHT = CONFIG.get('screen_height')

WINDOWED = CONFIG.get("windowed")
FPS = CONFIG.get('fps')
MUTED = CONFIG.get("muted")

""" PHYSICS"""
GRAVITY = pygame.Vector2((0, 0.3))

""" FONTS """
pygame.font.init()


def FONT(size, bold=False, italic=False, underline=False):
	font = pygame.font.Font("assets/fonts/HANDAGE.TTF", size)
	font.set_bold(bold)
	font.set_italic(italic)
	font.set_underline(underline)
	return font


def FONT_HIGH(size, bold=False, italic=False, underline=False):
	font = pygame.font.Font("assets/fonts/HANDAGE_HIGH.TTF", size)
	font.set_bold(bold)
	font.set_italic(italic)
	font.set_underline(underline)
	return font


""" COLORS """
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (30, 144, 255)
PURPLE = (155, 89, 182)
RED = (255, 0, 0)
GREEN = (60, 179, 113)
DARK_GREEN = (46, 139, 87)
FLASH_GREEN = (153, 255, 0)
ORANGE = (230, 140, 30)
GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
PINK = (255, 51, 153)
YELLOW = (241, 196, 15)

# https://flatuicolors.com/
# https://flatuicolors.com/palette/defo
TURQUOISE = (26, 188, 156)
CONCRETE = (149, 165, 166)
PUMPKIN = (211, 84, 0)
NICE_BLUE = (52, 152, 219)
MIDNIGHT_BLUE = (44, 62, 80)

COLORS = [
	BLACK, WHITE, GREY, LIGHT_GREY, CONCRETE,
	BLUE, TURQUOISE, NICE_BLUE, MIDNIGHT_BLUE,
	PURPLE,
	RED, PINK,
	GREEN, DARK_GREEN, FLASH_GREEN,
	ORANGE, YELLOW, PUMPKIN,
]
