import pygame, my
from os import listdir
from random import uniform

SOUNDS = {}


def loadSounds(directory):
    pass


def play(sound, volume=0.8, varyVolume=False, loops=0):
    pass
    if not my.MUTED:
        if varyVolume:
            volume -= uniform(0.0, 0.2)
            if volume < 0.1: volume = 0.1
            SOUNDS[sound].set_volume(volume)
        SOUNDS[sound].play(loops)
