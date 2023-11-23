#!/usr/bin/env python
import threading
import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID="d8279af9837543de8eb55d64f77d082f"
CLIENT_SECRET="48b31b8a7c5e48318f0d0671d25a49db"

running = True
pause_button_pin=17
volume_up_button_pin=27
volume_down_button_pin=22

# Setup GPIO pins for buttons
GPIO.setmode(GPIO.BCM)  # Use the Broadcom pin numbering
GPIO.setup(volume_up_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin to be an input pin and set initial value to be pulled up (high)
GPIO.setup(volume_down_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pause_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback functions for button presses
def monitor_exit_button_combo():
    
    global running
    while running:
        GPIO.setmode(GPIO.BCM)
        if GPIO.input(volume_up_button_pin) == GPIO.LOW and GPIO.input(volume_down_button_pin) == GPIO.LOW:
            start_time = time.time()
            while GPIO.input(volume_up_button_pin) == GPIO.LOW and GPIO.input(volume_down_button_pin) == GPIO.LOW:
                # If both buttons are held for more than 3 seconds, set running to False
                if time.time() - start_time > 3:
                    print("Exiting program...")
                    running = False
                    # Stop the music and cleanup before exiting
                    sp.pause_playback(device_id=DEVICE_ID)
                    GPIO.cleanup()
                    return
                time.sleep(0.1)
        time.sleep(0.1)

def toggle_play_pause(channel):
    print("Play/Pause")
    try:
        # Check current playback state
        playback = sp.current_playback()
        if playback and playback['is_playing']:
            sp.pause_playback(device_id=DEVICE_ID)
        else:
            sp.start_playback(device_id=DEVICE_ID)
    except spotipy.exceptions.SpotifyException as e:
        print("An error occurred while toggling play/pause:", e)

def next_track():
    print("Skipping to next track")
    sp.next_track(device_id=DEVICE_ID)

def previous_track():
    print("Going back to previous track")
    sp.previous_track(device_id=DEVICE_ID)

# Modified volume control functions
def volume_up(channel):
    start_time = time.time()
    while GPIO.input(channel) == GPIO.LOW:
        if time.time() - start_time > 1:  # Adjust the time as needed
            next_track()
            return
        time.sleep(0.1)
    # If the button was not held long enough, adjust volume
    print("Volume goes UP")
    current_volume = sp.current_playback()['device']['volume_percent']
    sp.volume(min(current_volume + 10, 100), device_id=DEVICE_ID)

def volume_down(channel):
    start_time = time.time()
    while GPIO.input(channel) == GPIO.LOW:
        if time.time() - start_time > 1:  # Adjust the time as needed
            previous_track()
            return
        time.sleep(0.1)
    # If the button was not held long enough, adjust volume
    print("Volume goes DOWN")
    current_volume = sp.current_playback()['device']['volume_percent']
    sp.volume(max(current_volume - 10, 0), device_id=DEVICE_ID)

# Detect button presses
GPIO.add_event_detect(pause_button_pin, GPIO.FALLING, callback=toggle_play_pause, bouncetime=200)
GPIO.add_event_detect(volume_up_button_pin, GPIO.FALLING, callback=volume_up, bouncetime=200)
GPIO.add_event_detect(volume_down_button_pin, GPIO.FALLING, callback=volume_down, bouncetime=200)




while running:
    try:
        exit_thread = threading.Thread(target=monitor_exit_button_combo)
        exit_thread.start()
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        
        # create an infinite while loop that will always be waiting for a new scan
        lastid=0
        while running:
            
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            
            if(id!=lastid):
                # DONT include the quotation marks around the card's ID value, just paste the number
                if (id==330752882257):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing a lowlife
                    sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2kDApipZtTzjwGfKujcg2z'])
                    sleep(2)
                
                elif (id==605630789265):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an weird!
                    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:1KsMhtT6PWdFuMCiNLvWmP')
                    sleep(2)
                    
                elif (id==536894535266):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an happier
                    sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:0UNDrAptMY5glGrcdr93Kx'])
                    sleep(2)
                    
                elif (id==401502336567):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an dear evan
                    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:0LhDyJXelg31FKLW5GDcKi')
                    sleep(2)
                    
                elif (id==330736105042):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an fleabag
                    sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:3TFtD8GZNw9v6vVWr3hnWy'])
                    sleep(2)
                    
                elif (id==124577674754):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an al filo
                    sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:4bp2lS1LSotJkXHxngiJxn'])
                    sleep(2)
                    
                elif (id==811772442274):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an hamilton
                    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:1kCHru7uhxBUdzkm4gzRQc')
                    sleep(2)
                    
                elif (id==1017930872562):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an hated
                    sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2NNq2V3PD8u55LqGs8ImU1'])
                    sleep(2)
                    
                elif (id==880475141843):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an lhaine patagonia
                    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:3JjSWhes0uMj7k2QzFozgG')
                    sleep(2)
                    
                elif (id==124594451969):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an david
                    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:playlist:7eZobX39lbj1jqEXOmelCK')
                    sleep(2)
                    
                elif (id==222668437326):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an yungblud
                    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:3Hthv2JVzYaWq0TyElU5lF')
                    sleep(2)
                
                elif (id==222668437326):
                    exit()
                
                # continue adding as many "elifs" for songs/albums that you want to play
            else:
                print("Same ID, skipped")
            
            lastid=id
    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        # The cleanup logic will be handled by the exit thread, but we'll include it here too, in case of other exceptions
        if running:  # Check if the program is still running
            print("Cleaning up...")
            GPIO.cleanup()
        exit_thread.join()  # Wait for the exit thread to finish if it's still running