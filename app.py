#!/usr/bin/env python3
"""
StillHere - The Memorial Orchestrator
operator: Everett N. Christman
mission: Grief Processing / Memorial Automation
"""

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

# --- VOICE & EMPATHY ENGINE ---
def speak(text):
    """
    Uses the system's native Text-to-Speech to give Nana a voice.
    Optimized for macOS (Samantha/Ava) for immediate comfort.
    """
    try:
        if platform.system() == 'Darwin':
            # 'Samantha' is usually the default compassionate voice on Mac
            subprocess.run(['say', '-v', 'Samantha', text])
        elif platform.system() == 'Windows':
            # Fallback for Windows (PowerShell speech)
            cmd = f'Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}");'
            subprocess.run(["powershell", "-Command", cmd])
        else:
            # Linux fallback
            subprocess.run(['espeak', text])
    except Exception:
        pass # If voice fails, we silently continue with text

def type_writer(text, speed=0.04):
    """Writes text slowly to match the speaking cadence."""
    print(f"\n    >> {text}")
    # We don't sleep here per char because the voice takes time, 
    # strictly visual formatting.

def communicate(text):
    """Simultaneous Voice and Text."""
    type_writer(text)
    speak(text)

def gentle_pause(seconds=1):
    time.sleep(seconds)

def ensure_memories_folder():
    mem_path = Path("Memories")
    mem_path.mkdir(exist_ok=True)
    return mem_path

# --- PLAYBACK LOGIC ---
def play_memory(file_path):
    abs_path = os.path.abspath(file_path)
    communicate("Opening the memory now.")
    
    try:
        if platform.system() == 'Darwin':
            subprocess.run(['open', abs_path], check=True)
        elif platform.system() == 'Windows':
            os.startfile(abs_path)
        else:
            subprocess.run(['xdg-open', abs_path], check=True)
    except Exception:
        communicate("I placed the file in your folder.")

def reveal_in_finder(folder_path):
    abs_path = os.path.abspath(folder_path)
    if platform.system() == 'Darwin':
        subprocess.run(['open', abs_path])
    elif platform.system() == 'Windows':
        os.startfile(abs_path)

# --- MAIN EXPERIENCE ---
def run_guided():
    print("\n" + "="*60)
    print("    S T I L L   H E R E")
    print("="*60 + "\n")
    
    # THE INTRO
    communicate("I am sorry for your loss.")
    gentle_pause(0.5)
    communicate("My name is Nana Banana. I am here to help you carry this.")
    gentle_pause(0.5)
    communicate("You don't need to worry about the details. I will handle the technical parts.")
    
    # NAME
    communicate("First, just tell me. Who are we honoring today?")
    name = input("    [Name]: ")
    
    safe_filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    
    communicate(f"Thank you. Let's make something beautiful for {name}.")
    
    # COLLECTION
    communicate("Please, drag and drop the photo you want to use into this window. Then press Enter.")
    
    assets = []
    while True:
        path_input = input("    [File Path]: ").strip().strip("'").strip('"')
        if path_input and os.path.exists(path_input):
            assets.append(path_input)
            break
        elif not path_input:
            communicate("I didn't catch that. Please drag the photo in.")
        else:
            communicate("I cannot find that file. Please try again.")

    # CONTEXT (Optional)
    communicate("Is there a specific song or artist that reminds you of them? If not, just press Enter.")
    song_info = input("    [Song/Artist]: ")
    
    communicate("Understood.")

    # FORMAT ( simplified for grief mode - defaulting to high quality)
    communicate("I am preparing the video for your iPhone and computer.")
    extension = "mov"
    
    # ORCHESTRATION
    communicate(f"Please wait a moment. I am weaving the memory for {name}.")
    
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
                'song': song_info,
                'artist': "" 
            }
            
            print("    [Processing...]")
            response = requests.post(API_URL, files=files, data=data)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.content)
                communicate("It is finished.")
            else:
                communicate("I had a small trouble with the engine, but I am still here.")
                print(f"    Debug: {response.text}")
                return

    except requests.exceptions.ConnectionError:
        communicate("I cannot reach the engine. Please make sure the server script is running.")
        return

    # PLAYBACK
    communicate("Would you like to see it now? Type yes or no.")
    if input("    >> ").lower().startswith('y'):
        play_memory(str(output_path))
    
    communicate("I have saved this in your Memories folder.")
    communicate("Take your time. I am signing off, but I am always here.")
    
    gentle_pause(2)
    reveal_in_finder(str(memories_dir))

if __name__ == '__main__':
    try:
        run_guided()
    except KeyboardInterrupt:
        sys.exit(0)
