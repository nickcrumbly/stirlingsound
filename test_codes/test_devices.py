# This code tests the devices available for mixer to help diagnosis of faults
# See https://stackoverflow.com/a/71304418 and https://stackoverflow.com/a/64923398
#pylint: disable=too-many-arguments
#pylint: disable=too-many-branches
#pylint: disable=too-many-boolean-expressions

import sys
import pygame
import pygame._sdl2.audio as sdl2_audio

pygame.mixer.init()
print("Start.")
print(sdl2_audio.get_audio_device_names(False))


pygame.quit()
