#!/usr/bin/env python
import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import pygame  # Import pygame for playing music
from time import sleep

# Initialize the mixer module
pygame.mixer.init()
running = True
pause_button_pin = 17
volume_up_button_pin = 27
volume_down_button_pin = 22

# Setup GPIO pins for buttons
GPIO.setmode(GPIO.BCM)  # Use the Broadcom pin numbering
GPIO.setup(volume_up_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(volume_down_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pause_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback functions for button presses

def check_exit_conditions():
    start_time = time.time()
    while GPIO.input(volume_up_button_pin) == GPIO.LOW and GPIO.input(volume_down_button_pin) == GPIO.LOW:
        if (time.time() - start_time) > 3:  # Check if buttons are held for more than 3 seconds
            print("Exiting program...")
            global running
            running = False
            break
        sleep(0.1)

def toggle_play_pause(channel):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def volume_up(channel):
    check_exit_conditions()  # Call this function to check if both buttons are being pressed
    print("Volume goes UP")
    current_volume = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(min(current_volume + 0.2, 1.0))

def volume_down(channel):
    check_exit_conditions()  # Call this function to check if both buttons are being pressed
    print("Volume goes DOWN")
    current_volume = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(max(current_volume - 0.2, 0.0))

# Detect button presses
GPIO.add_event_detect(pause_button_pin, GPIO.FALLING, callback=toggle_play_pause, bouncetime=200)
GPIO.add_event_detect(volume_up_button_pin, GPIO.FALLING, callback=volume_up, bouncetime=200)
GPIO.add_event_detect(volume_down_button_pin, GPIO.FALLING, callback=volume_down, bouncetime=200)

reader = SimpleMFRC522()

try:
    # create an infinite while loop that will always be waiting for a new scan
    lastid = 0
    while running:
        print("Waiting for record scan...")
        id, text = reader.read()
        print("Card Value is:", id)

        if id != lastid:
            if id == 330752882257:
                pygame.mixer.music.load('Music/song1.mp3')
                pygame.mixer.music.play()
                
            elif id == 605630789265:
                pygame.mixer.music.load('Music/song2.mp3')
                pygame.mixer.music.play()
            
            elif (id==222668437326):
                    exit()
            # continue adding as many "elifs" for songs/albums that you want to play
            
            sleep(2)  # Sleep to allow the music to start playing before re-enabling scanning
        else:
            print("Same ID, skipped")
        
        lastid = id
except KeyboardInterrupt:
    print("Program interrupted by user")
    
except Exception as e:
    print(e)

finally:
    print("Cleaning up...")
    GPIO.cleanup()
    pygame.mixer.quit()
