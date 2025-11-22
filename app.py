#!/usr/bin/env python3
"""
StillHere - The Memorial Orchestrator
V3.0 - Batch Processing & Natural Voice
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

# --- VOICE ENGINE (NATURAL) ---
def speak(text):
    """
    Uses the system default voice to avoid 'War Games' robotic sounds.
    """
    try:
        if platform.system() == 'Darwin':
            # Removing '-v Samantha' allows macOS to use your preferred System Voice (Siri/Enhanced)
            subprocess.run(['say', text])
        elif platform.system() == 'Windows':
            cmd = f'Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}");'
            subprocess.run(["powershell", "-Command", cmd])
    except Exception:
        pass 

def type_writer(text):
    print(f"\n    >> {text}")

def communicate(text):
    type_writer(text)
    speak(text)

def clean_path(path_input):
    """
    Fixes the 'File Not Found' error by removing Mac terminal escape characters.
    """
    if not path_input: return ""
    # Remove wrapping quotes
    clean = path_input.strip().strip("'").strip('"')
    # Remove the backslash used to escape spaces on Mac (e.g. "My\ Photo.jpg" -> "My Photo.jpg")
    clean = clean.replace("\\ ", " ") 
    # Just in case there are rogue backslashes left (careful with this one)
    clean = clean.replace("\\", "") 
    return clean

def ensure_memories_folder():
    mem_path = Path("Memories")
    mem_path.mkdir(exist_ok=True)
    return mem_path

# --- PLAYBACK LOGIC ---
def play_video(file_path):
    abs_path = os.path.abspath(file_path)
    try:
        if platform.system() == 'Darwin':
            subprocess.run(['open', abs_path])
        elif platform.system() == 'Windows':
            os.startfile(abs_path)
    except Exception:
        pass

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
    
    communicate("I am ready. We are going to handle multiple memories.")
    
    # NAME
    communicate("Who are we honoring?")
    name = input("    [Name]: ")
    safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    
    # BATCH COLLECTION LOOP
    assets = []
    communicate(f"Okay. Drag your photos or videos here, one by one.")
    communicate("Press Enter after each file. When you are done, just press Enter on a blank line.")
    
    while True:
        raw_input = input(f"    [File #{len(assets)+1}]: ")
        
        # 1. Check if user is done
        if not raw_input:
            if len(assets) > 0:
                break
            else:
                communicate("I need at least one file to begin.")
                continue
        
        # 2. Clean and Verify Path
        file_path = clean_path(raw_input)
        
        if os.path.exists(file_path):
            assets.append(file_path)
            print(f"       -> Added: {os.path.basename(file_path)}")
        else:
            communicate("I can't find that file. Try dragging it in again.")
            print(f"       (Debug: System saw path as: {file_path})")

    communicate(f"I have {len(assets)} memories collected.")

    # CONTEXT
    communicate("Is there a song or artist for these? If not, press Enter.")
    song_info = input("    [Song/Artist]: ")
    
    # EXECUTION LOOP
    communicate("I am starting the work. This might take a moment for each one.")
    
    memories_dir = ensure_memories_folder()
    completed_files = []

    for index, target_file in enumerate(assets):
        print(f"\n    --- Processing File {index + 1}/{len(assets)} ---")
        
        # Generate output name (e.g. Name_1.mov, Name_2.mov)
        extension = "mov"
        output_filename = f"{safe_name}_{index + 1}.{extension}"
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
                
                response = requests.post(API_URL, files=files, data=data)
                
                if response.status_code == 200:
                    with open(output_path, 'wb') as out_file:
                        out_file.write(response.content)
                    print(f"    -> Finished: {output_filename}")
                    completed_files.append(output_path)
                else:
                    print(f"    [!] Error on file {index+1}: {response.text}")

        except Exception as e:
            print(f"    [!] Connection failed on file {index+1}: {e}")

    # FINISH
    communicate("All tasks are complete.")
    
    if completed_files:
        communicate("I am opening the folder for you now.")
        reveal_in_finder(str(memories_dir))
        
        # Optional: Play the first one
        communicate("Would you like to watch the first one? (yes/no)")
        if input("    >> ").lower().startswith('y'):
            play_video(str(completed_files[0]))

    communicate("I am still here if you need more.")

if __name__ == '__main__':
    try:
        run_guided()
    except KeyboardInterrupt:
        sys.exit(0)
