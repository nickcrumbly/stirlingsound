#pylint: disable=too-many-arguments
#pylint: disable=too-many-branches
#pylint: disable=too-many-boolean-expressions

import sys
import random
import pygame
import glob
from gpiozero import Button, Device
import os

os.environ['SDL_VIDEODRIVER'] = "dummy"
testmode = os.environ.get('SRPS_PC_TEST')

# To drive from PC
if testmode:
    print("TESTMODE")
    from gpiozero.pins.mock import MockFactory
    Device.pin_factory = MockFactory()



# Initialize pygame mixer to have 5.1 channels
pygame.mixer.pre_init(channels=6, frequency=22500)
pygame.init()

screen = pygame.display.set_mode((500,500))

ichan = pygame.mixer.set_reserved(2)
if ichan != 2:
    print("Error, cannot reserve two playback channels")
    sys.exit()

ichan = pygame.mixer.Channel(0) # For the inspector sounds.
tchan = pygame.mixer.Channel(1) # For the train sounds.

boot_sound = pygame.mixer.Sound('inspector/allaboard_22k5.wav')
if not testmode:
    print("LIVE")
    ichan.play(boot_sound) # PC Testing



# Load the sounds
# Use 22500 Hz Wav files to reduce filesize whilst maintaining fidelity
pass_files = glob.glob('./pass/?pass?_22k5.wav')
print(pass_files)
start_files = glob.glob('./start/?start?_22k5.wav')
print(start_files)

passes = []
starts = []

for i in pass_files:
    passes.append(pygame.mixer.Sound(i))

for i in start_files:
    starts.append(pygame.mixer.Sound(i))

# Load the inspector
# Use 22500 Hz Wav files to reduce filesize whilst maintaining fidelity
inspA = pygame.mixer.Sound('inspector/clipA_22k5.wav')
inspB = pygame.mixer.Sound('inspector/clipB_22k5.wav')
inspC = pygame.mixer.Sound('inspector/clipC_22k5.wav')
inspD = pygame.mixer.Sound('inspector/clipD_22k5.wav')
inspE = pygame.mixer.Sound('inspector/clipE_22k5.wav')


# State Flags
LEVER1_4S = False
LEVER1_35S = False
LEVER2_4S = False
LEVER2_35S = False
LEVER3_4S = False
LEVER3_35S = False
INSPECTED = False


# Levers Pulled
lever1_pulled_type = pygame.event.custom_type()
event_pulled1 = pygame.event.Event(lever1_pulled_type)

lever2_pulled_type = pygame.event.custom_type()
event_pulled2 = pygame.event.Event(lever2_pulled_type)

lever3_pulled_type = pygame.event.custom_type()
event_pulled3 = pygame.event.Event(lever3_pulled_type)

# Levers Normal
lever1_normal_type = pygame.event.custom_type()
event_normal1 = pygame.event.Event(lever1_normal_type)

lever2_normal_type = pygame.event.custom_type()
event_normal2 = pygame.event.Event(lever2_normal_type)

lever3_normal_type = pygame.event.custom_type()
event_normal3 = pygame.event.Event(lever3_normal_type)

# 4s timers
LEVER1_4S_type = pygame.event.custom_type()
event_4s_lever1 = pygame.event.Event(LEVER1_4S_type)

# 35s timers
LEVER1_35S_type = pygame.event.custom_type()
event_35s_lever1 = pygame.event.Event(LEVER1_35S_type)

# 4s timers
LEVER2_4S_type = pygame.event.custom_type()
event_4s_lever2 = pygame.event.Event(LEVER2_4S_type)

# 35s timers
LEVER2_35S_type = pygame.event.custom_type()
event_35s_lever2 = pygame.event.Event(LEVER2_35S_type)


# 4s timers
LEVER3_4S_type = pygame.event.custom_type()
event_4s_lever3 = pygame.event.Event(LEVER3_4S_type)

# 35s timers
LEVER3_35S_type = pygame.event.custom_type()
event_35s_lever3 = pygame.event.Event(LEVER3_35S_type)



tevent_t = pygame.event.custom_type()
tevent = pygame.event.Event(tevent_t)



def btnpressed(switch):
    #print("Switch " + str(switch.pin.number) + " pressed")
    if switch.pin.number == 2:
        pygame.event.post(event_pulled1)
    elif switch.pin.number == 3:
        pygame.event.post(event_pulled2)
    elif switch.pin.number == 4:
        pygame.event.post(event_pulled3)
    else:
        print("Unknown input")


def btnreleased(switch):
    #print("Switch " + str(switch.pin.number) + " released")
    if switch.pin.number == 2:
        pygame.event.post(event_normal1)
    elif switch.pin.number == 3:
        pygame.event.post(event_normal2)
    elif switch.pin.number == 4:
        pygame.event.post(event_normal3)
    else:
        print("Unknown input")


def released(lever):
    global LEVER1_4S
    global LEVER1_35S
    global LEVER2_4S
    global LEVER2_35S
    global LEVER3_4S
    global LEVER3_35S
    global INSPECTED

    print("\nReleased: ", lever)
    diagp()

    if lever == 1:
        # 0 - 4 seconds in
        if not LEVER1_4S and not LEVER1_35S:
            tchan.fadeout(1000)
            LEVER1_4S = False
            LEVER1_35S = False
            pygame.time.set_timer(event_4s_lever1, 0)
            pygame.time.set_timer(event_35s_lever1, 0)
            if not ichan.get_busy() and not INSPECTED and not (switch2.is_pressed or switch3.is_pressed):
                ichan.play(inspA)
            elif not ichan.get_busy() and INSPECTED and not (switch2.is_pressed or switch3.is_pressed):
            	INSPECTED = False

        # 4 - 35 seconds in
        if LEVER1_4S and not LEVER1_35S:
            tchan.fadeout(1000)
            LEVER1_4S = False
            LEVER1_35S = False
            pygame.time.set_timer(event_35s_lever1, 0)
            if not ichan.get_busy() and not INSPECTED and not (switch2.is_pressed or switch3.is_pressed):
                ichan.play(inspB)
            elif not ichan.get_busy() and INSPECTED and not (switch2.is_pressed or switch3.is_pressed):
            	INSPECTED = False

        if LEVER1_35S:
            LEVER1_4S = False
            LEVER1_35S = False


    if lever == 2:
        # 0 - 4 seconds in
        if not LEVER2_4S and not LEVER2_35S:
            tchan.fadeout(1000)
            LEVER2_4S = False
            LEVER2_35S = False
            pygame.time.set_timer(event_4s_lever2, 0)
            pygame.time.set_timer(event_35s_lever2, 0)
            if not ichan.get_busy() and not INSPECTED and not (switch1.is_pressed or switch3.is_pressed):
                ichan.play(inspA)
            elif not ichan.get_busy() and INSPECTED and not (switch1.is_pressed or switch3.is_pressed):
            	INSPECTED = False


        # 4 - 35 seconds in
        if LEVER2_4S and not LEVER2_35S:
            tchan.fadeout(1000)
            LEVER2_4S = False
            LEVER2_35S = False
            pygame.time.set_timer(event_35s_lever2, 0)
            if not ichan.get_busy() and not INSPECTED and not (switch1.is_pressed or switch3.is_pressed):
                ichan.play(inspB)
            elif not ichan.get_busy() and INSPECTED and not (switch1.is_pressed or switch3.is_pressed):
            	INSPECTED = False


        if LEVER2_35S:
            LEVER2_4S = False
            LEVER2_35S = False



    if lever == 3:
        # 0 - 4 seconds in
        if not LEVER3_4S and not LEVER3_35S:
            tchan.fadeout(1000)
            LEVER3_4S = False
            LEVER3_35S = False
            pygame.time.set_timer(event_4s_lever3, 0)
            pygame.time.set_timer(event_35s_lever3, 0)
            if not ichan.get_busy() and not INSPECTED and not (switch1.is_pressed or switch2.is_pressed):
                ichan.play(inspA)
            elif not ichan.get_busy() and INSPECTED and not (switch1.is_pressed or switch2.is_pressed):
            	INSPECTED = False


        # 4 - 35 seconds in
        if LEVER3_4S and not LEVER3_35S:
            tchan.fadeout(1000)
            LEVER3_4S = False
            LEVER3_35S = False
            pygame.time.set_timer(event_35s_lever3, 0)
            if not ichan.get_busy() and not INSPECTED and not (switch1.is_pressed or switch2.is_pressed):
                ichan.play(inspB)
            elif not ichan.get_busy() and INSPECTED and not (switch1.is_pressed or switch2.is_pressed):
            	INSPECTED = False


        if LEVER3_35S:
            LEVER3_4S = False
            LEVER3_35S = False



def pulled(lever):
    global INSPECTED

    print("\nPulled: ", lever)
    diagp()

    if lever == 1:
        if switch2.is_pressed and switch3.is_pressed:
            tchan.fadeout(100)
            ichan.fadeout(100)
            INSPECTED = True
            ichan.play(inspE)
        elif (not LEVER2_4S and not LEVER2_35S and switch2.is_pressed) != (not LEVER3_4S and not LEVER3_35S and switch3.is_pressed):
            tchan.fadeout(1000)
            pygame.time.set_timer(event_4s_lever2, 0)
            pygame.time.set_timer(event_4s_lever3, 0)
            pygame.time.set_timer(event_35s_lever2, 0)
            pygame.time.set_timer(event_35s_lever3, 0)
            INSPECTED = True
            ichan.play(inspC)
        elif (LEVER2_4S and not LEVER2_35S and switch2.is_pressed) != (LEVER3_4S and not LEVER3_35S and switch3.is_pressed):
            tchan.fadeout(1000)
            pygame.time.set_timer(event_35s_lever2, 0)
            pygame.time.set_timer(event_35s_lever3, 0)
            INSPECTED = True
            ichan.play(inspD)
        elif (LEVER2_35S and switch2.is_pressed) != (LEVER3_35S and switch3.is_pressed):
            tchan.fadeout(1000)
            INSPECTED = True
            ichan.play(inspD)
        elif ((not LEVER2_35S or not LEVER3_35S) and switch2.is_pressed and switch3.is_pressed):
            ichan.stop()
            ichan.play(inspE)
        elif ((LEVER2_35S or LEVER3_35S) and switch2.is_pressed and switch3.is_pressed):
            tchan.fadeout(1000)
            ichan.play(inspE)
        else:
            tchan.play(random.choice(starts))
            pygame.time.set_timer(event_4s_lever1, 4000, loops=1)
            pygame.time.set_timer(event_35s_lever1, 35000, loops=1)


    if lever == 2:
        if switch1.is_pressed and switch3.is_pressed:
            tchan.fadeout(100)
            ichan.fadeout(100)
            INSPECTED = True
            ichan.play(inspE)
        elif (not LEVER1_4S and not LEVER1_35S and switch1.is_pressed) != (not LEVER3_4S and not LEVER3_35S and switch3.is_pressed):
            tchan.fadeout(1000)
            pygame.time.set_timer(event_4s_lever1, 0)
            pygame.time.set_timer(event_4s_lever3, 0)
            pygame.time.set_timer(event_35s_lever1, 0)
            pygame.time.set_timer(event_35s_lever3, 0)
            INSPECTED = True
            ichan.play(inspC)
        elif (LEVER1_4S and not LEVER1_35S and switch1.is_pressed) != (LEVER3_4S and not LEVER3_35S and switch3.is_pressed):
            tchan.fadeout(1000)
            pygame.time.set_timer(event_35s_lever1, 0)
            pygame.time.set_timer(event_35s_lever3, 0)
            INSPECTED = True
            ichan.play(inspD)
        elif (LEVER1_35S and switch1.is_pressed) != (LEVER3_35S and switch3.is_pressed):
            tchan.fadeout(1000)
            INSPECTED = True
            ichan.play(inspD)
#        elif ((not LEVER1_35S or not LEVER3_35S) and switch1.is_pressed and switch3.is_pressed):
#            ichan.stop()
#            ichan.play(inspE)
#        elif ((LEVER1_35S or LEVER3_35S) and switch1.is_pressed and switch3.is_pressed):
#            tchan.fadeout(1000)
#            ichan.play(inspE)
        else:
            tchan.play(random.choice(passes))
            pygame.time.set_timer(event_4s_lever2, 4000, loops=1)
            pygame.time.set_timer(event_35s_lever2, 35000, loops=1)


    if lever == 3:
        if switch1.is_pressed and switch2.is_pressed:
            tchan.fadeout(100)
            ichan.fadeout(100)
            INSPECTED = True
            ichan.play(inspE)
        elif (not LEVER2_4S and not LEVER2_35S and switch2.is_pressed) != (not LEVER1_4S and not LEVER1_35S and switch1.is_pressed):
            tchan.fadeout(1000)
            pygame.time.set_timer(event_4s_lever2, 0)
            pygame.time.set_timer(event_4s_lever1, 0)
            pygame.time.set_timer(event_35s_lever2, 0)
            pygame.time.set_timer(event_35s_lever1, 0)
            INSPECTED = True
            ichan.play(inspC)
        elif (LEVER2_4S and not LEVER2_35S and switch2.is_pressed) != (LEVER1_4S and not LEVER1_35S and switch1.is_pressed):
            tchan.fadeout(1000)
            pygame.time.set_timer(event_35s_lever2, 0)
            pygame.time.set_timer(event_35s_lever1, 0)
            INSPECTED = True
            ichan.play(inspD)
        elif (LEVER1_35S and switch1.is_pressed) != (LEVER2_35S and switch2.is_pressed):
            tchan.fadeout(1000)
            INSPECTED = True
            ichan.play(inspD)
#        elif ((not LEVER1_35S or not LEVER2_35S) and switch1.is_pressed and switch2.is_pressed):
#            ichan.stop()
#            ichan.play(inspE)
#        elif ((LEVER1_35S or LEVER2_35S) and switch1.is_pressed and switch2.is_pressed):
#            tchan.fadeout(1000)
#            ichan.play(inspE)
        else:
            tchan.play(random.choice(passes))
            pygame.time.set_timer(event_4s_lever3, 4000, loops=1)
            pygame.time.set_timer(event_35s_lever3, 35000, loops=1)



def printout():
        print('Lever1: {:6s}\tLever2: {:6s}\tLever3: {:6s}\t\tTrainchan: {:6s}\tInspChan: {:6s}'.format(str(switch1.is_pressed), str(switch2.is_pressed), str(switch3.is_pressed), str(tchan.get_busy()), str(ichan.get_busy())))


def diagp():
    print('\nLever1: {:10s}\t4s: {:10s}\t35s: {:10s}\nLever2: {:10s}\t4s: {:10s}\t35s: {:10s}\nLever3: {:10s}\t4s: {:10s}\t35s: {:10s}\nTrainchan: {:10s}\tInspChan: {:10s}\n'.format(str(switch1.is_pressed), str(LEVER1_4S), str(LEVER1_35S), str(switch2.is_pressed), str(LEVER2_4S), str(LEVER2_35S), str(switch3.is_pressed), str(LEVER3_4S), str(LEVER3_35S), str(tchan.get_busy()), str(ichan.get_busy())))



switch1 = Button(2)
switch1.when_pressed = btnpressed
switch1.when_released = btnreleased

switch2 = Button(3)
switch2.when_pressed = btnpressed
switch2.when_released = btnreleased

switch3 = Button(4)
switch3.when_pressed = btnpressed
switch3.when_released = btnreleased

FPS = 10
clock = pygame.time.Clock()


l1pull_t = pygame.event.custom_type()
l1pull = pygame.event.Event(l1pull_t)

l1norm_t = pygame.event.custom_type()
l1norm = pygame.event.Event(l1norm_t)

l2pull_t = pygame.event.custom_type()
l2pull = pygame.event.Event(l2pull_t)

l2norm_t = pygame.event.custom_type()
l2norm = pygame.event.Event(l2norm_t)

l3pull_t = pygame.event.custom_type()
l3pull = pygame.event.Event(l3pull_t)

l3norm_t = pygame.event.custom_type()
l3norm = pygame.event.Event(l3norm_t)

diagp_t = pygame.event.custom_type()
diagpe = pygame.event.Event(diagp_t)

pgq_t = pygame.event.custom_type()
pgq = pygame.event.Event(pgq_t)

#pygame.quit()

def main():
    global LEVER1_4S
    global LEVER1_35S
    global LEVER2_4S
    global LEVER2_35S
    global LEVER3_4S
    global LEVER3_35S

    pygame.time.set_timer(tevent, 1000) # Printouts
    A = True

    try:
        while A:
            for event in pygame.event.get():

                # Lever1 Pulled
                if event.type == lever1_pulled_type:
                    pulled(1)

                # # Lever1 Normal
                if event.type == lever1_normal_type:
                    released(1)


                # Lever2 Pulled
                if event.type == lever2_pulled_type:
                    pulled(2)

                # # Lever2 Normal
                if event.type == lever2_normal_type:
                    released(2)


                # Lever3 Pulled
                if event.type == lever3_pulled_type:
                    pulled(3)

                # Lever3 Normal
                if event.type == lever3_normal_type:
                    released(3)

                # Regular timer printout
                if event.type == tevent_t:
                    printout()


                # Timer events
                if event.type == LEVER1_4S_type:
                    LEVER1_4S = True

                if event.type == LEVER1_35S_type:
                    LEVER1_35S = True

                if event.type == LEVER2_4S_type:
                    LEVER2_4S = True

                if event.type == LEVER2_35S_type:
                    LEVER2_35S = True

                if event.type == LEVER3_4S_type:
                    LEVER3_4S = True

                if event.type == LEVER3_35S_type:
                    LEVER3_35S = True


                ## For testing events - should never fire in normal use
                if event.type == l1pull_t:
                    switch1.pin.drive_low()

                if event.type == l1norm_t:
                    switch1.pin.drive_high()

                if event.type == l2pull_t:
                    switch2.pin.drive_low()

                if event.type == l2norm_t:
                    switch2.pin.drive_high()

                if event.type == l3pull_t:
                    switch3.pin.drive_low()

                if event.type == l3norm_t:
                    switch3.pin.drive_high()

                if event.type == pgq_t:
                    diagp()
                    A = False

                if event.type == diagp_t:
                    diagp()



        clock.tick(FPS)

    # When you press ctrl+c, this will be called
    finally:
        print("Byeee")
        pygame.quit()


if __name__ == "__main__":
    TEST = "Z"
    if len(sys.argv) == 2:
        TEST = str(sys.argv[1])

    if TEST == "A":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l1norm, 6000, loops=1) # Once
        pygame.time.set_timer(pgq, 25000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "B":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l1norm, 8000, loops=1) # Once
        pygame.time.set_timer(pgq, 25000, loops=1) # Once
        #inspB plays for 15 seconds

    if TEST == "C":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l3pull, 6000, loops=1) # Once
        pygame.time.set_timer(pgq, 12000, loops=1) # Once
        #inspC plays for 15 seconds

    if TEST == "D":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l3pull, 8000, loops=1) # Once
        pygame.time.set_timer(pgq, 12000, loops=1) # Once
        #inspD plays

    if TEST == "E":
        pygame.time.set_timer(l2pull, 3000, loops=1) # Once
        pygame.time.set_timer(l1pull, 8000, loops=1) # Once
        pygame.time.set_timer(pgq, 12000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "F":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l3pull, 8000, loops=1) # Once
        pygame.time.set_timer(pgq, 12000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "G":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l2pull, 4000, loops=1) # Once
        pygame.time.set_timer(pgq, 12000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "H":
        pygame.time.set_timer(l2pull, 3000, loops=1) # Once
        pygame.time.set_timer(l1pull, 4000, loops=1) # Once
        pygame.time.set_timer(pgq, 12000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "I":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l3pull, 4000, loops=1) # Once
        pygame.time.set_timer(pgq, 12000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "J":
        pygame.time.set_timer(l2pull, 3000, loops=1) # Once
        pygame.time.set_timer(l1pull, 39000, loops=1) # Once
        pygame.time.set_timer(l1norm, 50000, loops=1) # Once
        pygame.time.set_timer(pgq, 61000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "K":
        pygame.time.set_timer(l1pull, 3000, loops=1) # Once
        pygame.time.set_timer(l2pull, 39000, loops=1) # Once
        pygame.time.set_timer(l3pull, 45000, loops=1) # Once
        pygame.time.set_timer(pgq, 61000, loops=1) # Once
        #inspA plays for 15 seconds

    if TEST == "L":
        pygame.time.set_timer(l3pull, 3000, loops=1) # Once
        pygame.time.set_timer(l2pull, 8000, loops=1) # Once
        pygame.time.set_timer(l1pull, 12000, loops=1) # Once
        pygame.time.set_timer(pgq, 20000, loops=1) # Once
        #inspA plays for 15 seconds


    if TEST == "M":
        pygame.time.set_timer(l3pull, 3000, loops=1) # Once
        pygame.time.set_timer(diagpe, 50000, loops=1)
        pygame.time.set_timer(l3norm, 52000, loops=1) # Once
        pygame.time.set_timer(pgq, 55000, loops=1) # Once
        #inspA plays for 15 seconds

    # Problem2 of March2024 - Issue #2 on github
    if TEST == "N":
        pygame.time.set_timer(l1pull, 1000, loops=1)
        pygame.time.set_timer(l2pull, 3000, loops=1)
        pygame.time.set_timer(l1norm, 8000, loops=1)
        pygame.time.set_timer(l2norm, 10000, loops=1)
        pygame.time.set_timer(pgq, 12000, loops=1)
        #inspC should play and not get upset when you release levers

    # Problem3 of March2024 - Issue #3 on github
    if TEST == "O":
        pygame.time.set_timer(l2pull, 1000, loops=1)
        pygame.time.set_timer(l3pull, 8000, loops=1)
        pygame.time.set_timer(l3norm, 13000, loops=1)
        pygame.time.set_timer(l2norm, 15000, loops=1)
        pygame.time.set_timer(pgq, 18000, loops=1)
        #inspD should play and not get upset when you release levers

    # Problem4 of March2024 - Issue #4 on github
    if TEST == "P":
        pygame.time.set_timer(l1pull, 1000, loops=1)
        pygame.time.set_timer(l2pull, 3000, loops=1)
        pygame.time.set_timer(l3pull, 5000, loops=1)
        pygame.time.set_timer(l1norm, 10000, loops=1)
        pygame.time.set_timer(l2norm, 12000, loops=1)
        pygame.time.set_timer(l3norm, 13000, loops=1)
        pygame.time.set_timer(pgq, 17000, loops=1)
        #inspC should play once then be interrupted by inspE and not get upset when you release levers


    main()
