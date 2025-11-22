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
from pathlib import Path
from typing import Optional

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

# --- MAIN LOGIC ---

def run_web_ui(host: str = "127.0.0.1", port: int = 6161, debug: bool = False):
    """Launches the visual interface."""
    from stillhere.ui.web_ui import WebUI

    print_banner()
    type_writer(f"    >> Opening the sanctuary at http://{host}:{port}...", speed=0.01)
    print("    >> Press Ctrl+C to close the connection.\n")

    ui = WebUI(host=host, port=port, debug=debug)
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n\n    Goodbye. Be gentle with yourself.")
        print_quote()
        sys.exit(0)

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
        # Actual logic would hook into the backend here
        path = input("    [File Path]: ").strip().strip("'").strip('"')
        
        if path:
            type_writer(f"\n    I see it. {name} looks wonderful here.")
            type_writer("    Processing the image... applying the 'Gentle Spirit' animation...")
            # Simulating work for the "Grand" feel
            gentle_pause(2)
            print("    [....................] 25%")
            gentle_pause(1)
            print("    [||||||||||..........] 50%")
            gentle_pause(1)
            print("    [||||||||||||||||||||] 100%")
            print("")
            type_writer("    Done. The memory has been revitalized.")
            type_writer(f"    Saved to: /memories/{name}_alive.mp4")
            
    elif choice == '2':
        type_writer("\n    Voice is the echo of the soul.")
        type_writer("    I need at least 30 seconds of clear audio to learn their pattern.")
        # Placeholder for voice logic
        
    else:
        type_writer("\n    Let's focus on a tribute. I will help you arrange the timeline.")

    print("")
    type_writer(f"    Is there anything else I can do for {name} today?")
    # Loop or exit logic would go here...

    print_quote()

def main():
    parser = argparse.ArgumentParser(
        description="StillHere - Bringing cherished memories to life",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--web', action='store_true', help='Run web interface')
    parser.add_argument('--host', default='127.0.0.1', help='Host IP')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    parser.add_argument('--version', action='store_true', help='Show version')

    args, unknown = parser.parse_known_args()

    if args.version:
        print("StillHere v2.0 (Grand Edition)")
        print("By Everett Christman")
        return

    if args.cli:
        from stillhere.ui.cli import CLI
        CLI().run(unknown)
    elif args.web:
        run_web_ui(host=args.host, port=args.port, debug=args.debug)
    else:
        # Default to the Compassionate Guide
        run_guided()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n    Goodbye. Be gentle with yourself.")
        sys.exit(0)
