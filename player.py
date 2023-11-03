#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID="d8279af9837543de8eb55d64f77d082f"
CLIENT_SECRET="48b31b8a7c5e48318f0d0671d25a49db"

while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        # create an infinite while loop that will always be waiting for a new scan
        lastid=0
        while True:
            
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            
            if(id!=lastid):
                # DONT include the quotation marks around the card's ID value, just paste the number
                if (id==330752882257):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing a song
                    sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2vSLxBSZoK0eha4AuhZlXV'])
                    sleep(2)
                
                elif (id==605630789265):
                    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                    # playing an album
                    sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:0JGOiO34nwfUdDrD612dOp')
                    sleep(2)
                
                # continue adding as many "elifs" for songs/albums that you want to play
            else:
                print("Same ID, skipped")
            
            lastid=id
    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()