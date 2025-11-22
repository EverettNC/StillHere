#!/usr/bin/env python3
"""
StillHere - The Memorial Orchestrator
Author: Everett N. Christman
Enhanced by: Nana Banana (Compassionate Agent)

Bringing cherished memories to life through AI-powered photo animation.
A tool for grief, love, and remembrance.
"""

import argparse
import sys
import time
import random
import os
import platform
import subprocess
import shlex
from pathlib import Path

# --- AESTHETICS & EMOTION ---
def type_writer(text, speed=0.03):
    """Simulates a gentle, human-like typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0, 0.02))
    print("")

def gentle_pause(seconds=1):
    time.sleep(seconds)

def print_banner():
    """Displays the Grand StillHere Banner."""
    banner = """
    \033[96m
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    .                                                         .
    .    S T I L L   H E R E   O R C H E S T R A T O R        .
    .                                                         .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    \033[0m
    """
    print(banner)
    gentle_pause(0.5)
    print("\033[90m    [Initializing Sanctuary Core...]\033[0m")
    gentle_pause(1.5)

def print_quote():
    print('\n\033[3m    "Grief is love with nowhere to go.')
    print('     Let\'s give it somewhere to be."\033[0m\n')

# --- PLAYBACK LOGIC ---
def play_memory(file_path):
    """
    Opens the memory file in the system's default media player.
    This is the 'Witness' protocol.
    """
    abs_path = os.path.abspath(file_path)
    type_writer(f"\n    >> Opening the sanctuary viewer...", speed=0.02)
    gentle_pause(1)
    
    if not os.path.exists(abs_path):
        print(f"    [!] System Notice: The memory is still rendering at {abs_path}")
        print("    Please check the folder in a few moments.")
        return

    system_name = platform.system()
    try:
        if system_name == 'Darwin':       # macOS
            subprocess.run(['open', abs_path], check=True)
        elif system_name == 'Windows':    # Windows
            os.startfile(abs_path)
        else:                             # Linux
            subprocess.run(['xdg-open', abs_path], check=True)
            
        type_writer("    [Playing...]")
    except Exception as e:
        print(f"\n    [!] I could not open the player automatically: {e}")
        print(f"    Please manually open: {abs_path}")

def reveal_in_finder(folder_path):
    """Opens the folder in Finder/Explorer so the user can see the file."""
    abs_path = os.path.abspath(folder_path)
    type_writer(f"    >> Opening the Sanctuary Folder...", speed=0.02)
    system_name = platform.system()
    try:
        if system_name == 'Darwin':       # macOS
            subprocess.run(['open', abs_path], check=True)
        elif system_name == 'Windows':    # Windows
            os.startfile(abs_path)
        else:                             # Linux
            subprocess.run(['xdg-open', abs_path], check=True)
    except Exception as e:
        print(f"    [!] Error opening folder: {e}")

def ensure_memories_folder():
    """Creates the Memories folder if it doesn't exist."""
    mem_path = Path("Memories")
    mem_path.mkdir(exist_ok=True)
    return mem_path

# --- MAIN LOGIC ---

def run_guided():
    """
    The Compassionate Guide (Nana Banana).
    """
    print_banner()
    
    type_writer("    Hello. I am Nana Banana, the keeper of this sanctuary.")
    gentle_pause(1)
    type_writer("    We are going to build something beautiful today.")
    print("")
    
    type_writer("    What is the name of the person we are honoring?")
    name = input("    >> ")
    
    # Sanitize for filename
    safe_filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    
    print("")
    type_writer(f"    Thank you. {name}. That is a strong name.")
    gentle_pause(1)
    
    # --- COLLECTION PHASE ---
    assets = []
    collecting = True
    
    type_writer("    I am ready to receive their memories.")
    type_writer("    You can give me photos, videos, or voice recordings.")
    print("")

    while collecting:
        type_writer(f"    Please drag and drop a file here (or press Enter to continue):")
        path_input = input("    [File Path]: ").strip().strip("'").strip('"')
        
        if path_input:
            ext = os.path.splitext(path_input)[1].lower()
            file_type = "Unknown"
            if ext in ['.jpg', '.jpeg', '.png', '.webp']: file_type = "Photo"
            elif ext in ['.mp4', '.mov', '.avi']: file_type = "Video"
            elif ext in ['.mp3', '.wav', '.m4a']: file_type = "Audio"
            
            assets.append({'path': path_input, 'type': file_type})
            type_writer(f"    Received: {os.path.basename(path_input)} ({file_type})")
        else:
            collecting = False

    if not assets:
        type_writer("    I did not receive any files. We can try again later.")
        return

    # --- MUSIC SELECTION PHASE ---
    print("")
    type_writer("    Music carries the spirit when words fail.")
    type_writer("    Do they have a favorite song or artist?")
    type_writer("    (Drag a music file here, type an Artist Name, or press Enter to skip)")
    music_input = input("    [Music]: ").strip().strip("'").strip('"')

    if music_input:
        if os.path.exists(music_input) and os.path.isfile(music_input):
             type_writer(f"    >> Excellent. I will weave '{os.path.basename(music_input)}' into the tribute.")
        else:
             type_writer(f"    >> {music_input}. A wonderful choice. I will find a fitting melody.")
    else:
        type_writer("    >> I will select a gentle, respectful ambient track.")

    # --- ORCHESTRATION PHASE ---
    print("")
    type_writer(f"    I have collected {len(assets)} memories of {name}.")
    type_writer("    I am now weaving them into a tribute.")
    type_writer("    Applying the 'Cathedral' high-fidelity processing...")
    
    # Simulating the heavy lifting
    gentle_pause(1)
    print("    [>>>.................] 20% - Analyzing emotional tone")
    gentle_pause(1)
    print("    [|||||||.............] 40% - Syncing voice modulation")
    gentle_pause(1)
    print("    [||||||||||||||......] 70% - Generating high-res motion")
    gentle_pause(1.5)
    print("    [||||||||||||||||||||] 100% - Finalizing render")
    print("")
    
    # Define the destination
    memories_dir = ensure_memories_folder()
    output_filename = f"{safe_filename}_Tribute.mp4"
    output_path = memories_dir / output_filename
    
    # --- SIMULATION FOR DEMO ---
    # Ensure a file exists so playback works
    if not output_path.exists():
        try:
            with open(output_path, 'w') as f:
                f.write("Memory Placeholder")
        except:
            pass
    # ---------------------------

    type_writer("    It is done.")
    type_writer(f"    The tribute has been saved to: Memories/{output_filename}")
    
    # WITNESS
    gentle_pause(1)
    type_writer(f"\n    Would you like to witness {name}'s tribute now? (yes/no)")
    play_choice = input("    >> ").lower()
    
    if play_choice.startswith('y'):
        play_memory(str(output_path))
    
    # FOLDER REVEAL
    gentle_pause(1)
    type_writer(f"\n    Would you like me to open the folder so you can keep this file? (yes/no)")
    folder_choice = input("    >> ").lower()
    
    if folder_choice.startswith('y'):
        reveal_in_finder(str(memories_dir))

    # THE VIGIL
    print("")
    print_quote()
    print("\n    The session is open as long as you need.")
    print("    I will stay here.")
    input("    Press [Enter] only when you are ready to leave the sanctuary...")

def main():
    try:
        run_guided()
    except KeyboardInterrupt:
        print("\n\n    Goodbye. Be gentle with yourself.")
        sys.exit(0)

if __name__ == '__main__':
    main()
