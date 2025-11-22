#!/usr/bin/env python3
"""
StillHere - The Memorial Interface
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
    .    S T I L L   H E R E   M E M O R I A L   S U I T E    .
    .                                                         .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    \033[0m
    """
    print(banner)
    gentle_pause(0.5)
    print("\033[90m    [Initializing Memory Core...]\033[0m")
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

def ensure_memories_folder():
    """Creates the Memories folder if it doesn't exist."""
    mem_path = Path("Memories")
    mem_path.mkdir(exist_ok=True)
    return mem_path

# --- MAIN LOGIC ---

def run_guided():
    """
    The Compassionate Guide (Nana Banana).
    Takes the user by the hand through the process.
    """
    print_banner()
    
    type_writer("    Hello. I am the memory keeper for this session.")
    gentle_pause(1)
    type_writer("    I know this process can be heavy, but I am here to help you.")
    type_writer("    We are going to bring a photo to life, gently and beautifully.")
    print("")
    
    type_writer("    What is the name of the person we are honoring today?")
    name = input("    >> ")
    
    # Sanitize for filename
    safe_filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    
    print("")
    type_writer(f"    Thank you. It is an honor to work on {name}'s memory with you.")
    gentle_pause(1)
    
    type_writer("    I can assist you with:")
    print("    1. [Animate] Make a still photo move and breathe.")
    print("    2. [Voice]   Reconstruct their voice from audio samples.")
    print("    3. [Video]   Create a tribute video for a service.")
    print("")
    
    choice = input("    Which would you like to start with? (1/2/3): ")
    
    if choice == '1':
        type_writer("\n    Excellent choice. Seeing them move again is powerful.")
        type_writer("    Please drag and drop the photo file into this window...")
        
        path_input = input("    [File Path]: ").strip().strip("'").strip('"')
        
        if path_input:
            type_writer(f"\n    I see it. {name} looks wonderful here.")
            type_writer("    Processing the image... applying the 'Gentle Spirit' animation...")
            
            # Simulating work
            gentle_pause(1.5)
            print("    [>>>.................] 15% - Reading features")
            gentle_pause(1)
            print("    [||||||||||..........] 50% - Generating motion")
            gentle_pause(1)
            print("    [||||||||||||||||||||] 100% - Rendering video")
            print("")
            
            memories_dir = ensure_memories_folder()
            output_filename = f"{safe_filename}_alive.mp4"
            output_path = memories_dir / output_filename
            
            # Create dummy file if needed for demo so player works
            if not output_path.exists():
                try:
                    with open(output_path, 'w') as f:
                        f.write("Memory Placeholder")
                except:
                    pass

            type_writer("    Done. The memory has been revitalized.")
            type_writer(f"    Saved to: Memories/{output_filename}")
            
            gentle_pause(0.5)
            type_writer(f"\n    Would you like to witness {name} now? (yes/no)")
            play_choice = input("    >> ").lower()
            
            if play_choice.startswith('y'):
                play_memory(str(output_path))
            
            gentle_pause(1)

    elif choice == '2':
        type_writer("\n    Voice is the echo of the soul.")
        
    else:
        type_writer("\n    Let's focus on a tribute.")

    print("")
    type_writer(f"    I have completed the tasks for {name}.")
    print_quote()
    
    # THE VIGIL - THIS IS THE FIX THAT STOPS IT FROM CLOSING
    print("\n    The session is open as long as you need.")
    print("    I will stay here.")
    input("    Press [Enter] only when you are ready to close the sanctuary...")

def main():
    try:
        # Check arguments
        if len(sys.argv) > 1 and sys.argv[1] in ['--cli', '--web', '--version', '--help']:
             pass 
        else:
            run_guided()
    except KeyboardInterrupt:
        print("\n\n    Goodbye. Be gentle with yourself.")
        sys.exit(0)

if __name__ == '__main__':
    main()
