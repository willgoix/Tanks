import pygame, my
from os import listdir
from random import uniform

SOUNDS = {}

def loadSounds(directory):
	for filename in listdir(directory):
		SOUNDS[filename.split(".")[0]] = pygame.mixer.Sound('{}/{}'.format(directory, filename))


def play(sound, volume=0.8, varyVolume=True, loops=0):
	if not my.MUTED:
		if varyVolume:
			volume -= uniform(0.0, 0.2)
			if volume < 0.1: volume = 0.1
			SOUNDS[sound].set_volume(volume)
		SOUNDS[sound].play(loops)
