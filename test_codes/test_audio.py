# This code has the same startup routines as the main code so allows you to test functionality without loading the full thing.
# It plays the test sounds from Fraunhofer
#pylint: disable=too-many-arguments
#pylint: disable=too-many-branches
#pylint: disable=too-many-boolean-expressions

import sys
import random
import pygame
import glob
from gpiozero import Button, Device
import time

# Initialize pygame mixer to have 5.1 channels
pygame.mixer.pre_init(channels=6)
#pygame.mixer.pre_init(channels=2) # Use for testing with HDMI/Headphone options
pygame.init()

# Test multi-chan support in PyGame
ichan = pygame.mixer.set_reserved(2)
if ichan != 2:
    print("Error, cannot reserve two playback channels")
    sys.exit()

ichan = pygame.mixer.Channel(0) # For the inspector sounds.
tchan = pygame.mixer.Channel(1) # For the train sounds.


# Load the test sound
chid = pygame.mixer.Sound('ChID-BLITS-EBU-Narration441-16b.wav') 
# Note that this file must be downloaded from Fraunhofer
# https://www2.iis.fraunhofer.de/AAC/multichannel.html

chid.play()

while pygame.mixer.get_busy():
    time.sleep(1)
    print('.', end='', flush=True)

print('', flush=True)
pygame.quit()

