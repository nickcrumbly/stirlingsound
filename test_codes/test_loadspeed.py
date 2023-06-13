# This code has the same startup routines as the main code so allows you to test loading speed
# The code came from: https://realpython.com/python-timer
#pylint: disable=too-many-arguments
#pylint: disable=too-many-branches
#pylint: disable=too-many-boolean-expressions

import sys
import random
import pygame
import glob
import time


tic = time.perf_counter()

# Full form of pre_init syntax for reference:
# pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE)

# Initialize pygame mixer to have 5.1 channels
#pygame.mixer.pre_init(channels=6, frequency=22500)
pygame.mixer.pre_init(channels=2) # Use for testing with HDMI/Headphone options
pygame.init()

# Test multi-chan support in PyGame
ichan = pygame.mixer.set_reserved(2)
if ichan != 2:
    print("Error, cannot reserve two playback channels")
    sys.exit()

ichan = pygame.mixer.Channel(0) # For the inspector sounds.
tchan = pygame.mixer.Channel(1) # For the train sounds.


# Load the sounds
pass_files = glob.glob('./pass/?pass?.wav')
print(pass_files)
start_files = glob.glob('./start/?start?.wav')
print(start_files)

# Fixed imports
boot_sound = pygame.mixer.Sound('inspector/allaboard.wav')
inspA = pygame.mixer.Sound('inspector/clipA.wav')
inspB = pygame.mixer.Sound('inspector/clipB.wav')
inspC = pygame.mixer.Sound('inspector/clipC.wav')
inspD = pygame.mixer.Sound('inspector/clipD.wav')
inspE = pygame.mixer.Sound('inspector/clipE.wav')


passes = []
starts = []

for i in pass_files:
    passes.append(pygame.mixer.Sound(i))

for i in start_files:
    starts.append(pygame.mixer.Sound(i))

toc = time.perf_counter()
print(f"Loaded all files in {toc - tic:0.4f} seconds")

pygame.quit()

