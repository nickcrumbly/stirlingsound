#pylint: disable=too-many-arguments
#pylint: disable=too-many-branches
#pylint: disable=too-many-boolean-expressions

import sys
import random
import pygame
import glob

# Load the sounds
pass_files = glob.glob('./pass/*.wav')
print(pass_files)
start_files = glob.glob('./start/*.wav')
print(start_files)

passes = []
starts = []

#for i in pass_files:
#    passes.append(pygame.mixer.Sound(i))

#for i in start_files:
#    starts.append(pygame.mixer.Sound(i))



for i in range(len(starts)):
    print(random.choice(starts))

for i in range(len(passes)):
    print(random.choice(passes))

