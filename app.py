#!/usr/bin/env python3
"""
StillHere - The Memorial Orchestrator
Author: Everett N. Christman
Enhanced by: Nana Banana (Compassionate Agent)
"""

import argparse
import sys
import time
import random
import os
import platform
import subprocess
import requests
from pathlib import Path

# --- CONFIGURATION ---
API_URL = "http://localhost:8282/api/animate"

# --- HELPERS ---
def type_writer(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0, 0.02))
    print("")

def gentle_pause(seconds=1):
    time.sleep(seconds)

def print_banner():
    print("\n" + "="*60)
    print("    S T I L L   H E R E   O R C H E S T R A T O R")
    print("="*60)
    gentle_pause(0.5)
    print("    [Initializing Sanctuary Core...]\n")
    gentle_pause(1.5)

def print_quote():
    print('\n    "Grief is love with nowhere to go.')
    print('     Let\'s give it somewhere to be."\n')

def ensure_memories_folder():
    mem_path = Path("Memories")
    mem_path.mkdir(exist_ok=True)
    return mem_path

# --- PLAYBACK LOGIC ---
def play_memory(file_path):
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        print(f"    [!] File not found: {abs_path}")
        return

    type_writer(f"\n    >> Opening viewer...", speed=0.02)
    
    system_name = platform.system()
    try:
        if system_name == 'Darwin':       # macOS
            subprocess.run(['open', abs_path], check=True)
        elif system_name == 'Windows':    # Windows
            os.startfile(abs_path)
        else:                             # Linux
            subprocess.run(['xdg-open', abs_path], check=True)
    except Exception as e:
        print(f"    [!] Manual Open Required: {abs_path}")

def reveal_in_finder(folder_path):
    abs_path = os.path.abspath(folder_path)
    type_writer(f"    >> Opening folder...", speed=0.02)
    try:
        if platform.system() == 'Darwin':
            subprocess.run(['open', abs_path])
        elif platform.system() == 'Windows':
            os.startfile(abs_path)
        else:
            subprocess.run(['xdg-open', abs_path])
    except Exception as e:
        print(f"    [!] Could not open folder: {e}")

# --- MAIN LOGIC ---
def run_guided():
    print_banner()
    
    type_writer("    Hello. I am Nana Banana, the keeper of this sanctuary.")
    gentle_pause(1)
    type_writer("    We are going to build a tribute worthy of the life lived.")
    print("")
    
    type_writer("    What is the name of the person we are honoring?")
    name = input("    >> ")
    
    safe_filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    
    print("")
    type_writer(f"    Thank you. {name}.")
    gentle_pause(1)
    
    # --- COLLECTION LOOP ---
    assets = []
    collecting = True
    
    type_writer("    I am ready to receive memories (Photos).")
    print("")

    # Currently accepting single file for the V2 prototype
    while collecting:
        type_writer(f"    Drag and drop a photo here (or press Enter to finish):")
        path_input = input("    [File Path]: ").strip().strip("'").strip('"')
        
        if path_input:
            if os.path.exists(path_input):
                assets.append(path_input)
                type_writer(f"    >> Received memory.")
                collecting = False # Enforce single file for now
            else:
                type_writer(f"    [!] I cannot find that file. Please try again.")
        else:
            collecting = False

    if not assets:
        type_writer("    No files received. Restarting session...")
        return

    # --- MUSIC SELECTION ---
    print("")
    type_writer("    Do they have a favorite song or artist?")
    
    song_name = input("    [Song Name]: ").strip()
    artist_name = input("    [Artist Name]: ").strip()

    if song_name or artist_name:
        type_writer(f"    >> Soundtrack context set: {song_name} // {artist_name}")

    # --- FORMAT SELECTION ---
    print("")
    type_writer("    How should I save this tribute?")
    type_writer("    1. MOV (Best for Apple/QuickTime/iPhone)")
    type_writer("    2. MP4 (Universal)")
    fmt_choice = input("    [1 or 2]: ").strip()
    
    extension = "mov" if fmt_choice == "1" else "mp4"
    
    # --- ORCHESTRATION (THE REAL API CALL) ---
    print("")
    type_writer(f"    Weaving memories for {name}...")
    type_writer("    Connecting to the Engine (Port 8282)...")
    
    # Prepare Data
    target_file = assets[0]
    memories_dir = ensure_memories_folder()
    output_filename = f"{safe_filename}_Tribute.{extension}"
    output_path = memories_dir / output_filename

    try:
        with open(target_file, 'rb') as f:
            files = {'photo': f}
            data = {
                'style': 'gentle_smile',
                'duration': 5,
                'format': extension,
                'song': song_name,
                'artist': artist_name
            }
            
            # Simulate progress while waiting for server
            print("    [..........] Sending Data")
            response = requests.post(API_URL, files=files, data=data, stream=True)
            
            if response.status_code == 200:
                print("    [||||||||||] Rendering Complete")
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.content)
                type_writer("    It is done.")
            else:
                print(f"    [!] Engine Error: {response.status_code} - {response.text}")
                return

    except requests.exceptions.ConnectionError:
        print("    [!] ERROR: Could not connect to 'api_server.py'.")
        print("    [!] Please ensure the Engine is running in a separate terminal.")
        return
    except Exception as e:
        print(f"    [!] Unexpected Error: {e}")
        return

    # --- WITNESS ---
    type_writer(f"\n    Would you like to witness {name}'s tribute now? (yes/no)")
    if input("    >> ").lower().startswith('y'):
        play_memory(str(output_path))
    
    # --- FOLDER ---
    type_writer(f"\n    Open the folder to keep this file? (yes/no)")
    if input("    >> ").lower().startswith('y'):
        reveal_in_finder(str(memories_dir))

    # --- VIGIL ---
    print("")
    print_quote()
    print("\n    The session is open. I will stay here.")
    input("    Press [Enter] only when you are ready to leave...")

if __name__ == '__main__':
    try:
        run_guided()
    except KeyboardInterrupt:
        print("\n    Goodbye.")
        sys.exit(0)
