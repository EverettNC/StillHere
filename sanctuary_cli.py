#!/usr/bin/env python3
import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
import textwrap

# --- CONFIGURATION ---
# NATIVE MAC VOICE (System Default - Siri/Samantha)
# No robotic "War Games" voice.
def speak(text):
    # -r 175 slows it down slightly for a more conversational pace
    os.system(f"say -r 175 '{text}' &")

def type_writer(text, speed=0.04):
    """Writes text to the terminal like a person speaking."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print("")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def gentle_input(prompt_text):
    """Asks a question gently, speaking it first."""
    speak(prompt_text)
    type_writer(f"\n    >> {prompt_text}")
    return input("       > ").strip()

# --- ENGINE TOOLS ---

def check_dependencies():
    """Ensures we have the tools to honor her properly."""
    missing = []
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg")
    
    # Check for yt-dlp (Python lib)
    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp")
        
    if missing:
        print(f"\n[!] I am missing tools: {', '.join(missing)}")
        print("    Please run: pip install yt-dlp")
        print("    And ensure ffmpeg is installed (brew install ffmpeg)")
        sys.exit(1)

def fetch_song_cli(query):
    """The Agent goes to find the music."""
    import yt_dlp
    
    print(f"\n    [Orchestrating Music: '{query}']")
    speak(f"I am finding {query} for you now.")
    
    temp_audio = "temp_sanctuary_audio"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_audio,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query} audio"])
        return f"{temp_audio}.mp3"
    except Exception as e:
        print(f"    [!] Could not retrieve music: {e}")
        return None

def clean_path(path_input):
    """Cleans Mac terminal drag-and-drop artifacts."""
    if not path_input: return ""
    clean = path_input.strip().strip("'").strip('"')
    clean = clean.replace("\\ ", " ")
    clean = clean.replace("\\", "")
    return clean

# --- THE CORE RITUAL ---

def render_tribute(image_path, audio_path, output_folder, index, total):
    """
    High Fidelity ProRes Render.
    Static. Respectful. 1080p.
    """
    clean_name = image_path.stem
    safe_name = f"{clean_name}_Tribute.mov"
    output_path = output_folder / safe_name
    
    # 1. Inputs
    inputs = ['-loop', '1', '-i', str(image_path), '-i', str(audio_path)]
    
    # 2. Filter (Scale to 1080p, Fade In, NO SHAKE)
    # This centers the image and adds black bars if needed (Letterboxing) to preserve aspect ratio
    filter_complex = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fade=in:0:30"

    cmd = [
        "ffmpeg", '-y',
        *inputs,
        '-vf', filter_complex,
        '-c:v', 'prores_ks', '-profile:v', '2', # Apple ProRes Standard
        '-c:a', 'pcm_s16le',                    # Uncompressed Audio
        '-map', '0:v', '-map', '1:a',
        '-shortest',                            # End when song ends
        str(output_path)
    ]
    
    try:
        # Run silently
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    [{index}/{total}] Completed: {safe_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"    [!] Failed to render: {safe_name}")
        return False

# --- THE GUIDE ---

def main():
    clear_screen()
    check_dependencies()
    
    print("\n" + "="*60)
    print("    S T I L L   H E R E   (Terminal Sanctuary)")
    print("="*60)
    
    # INTRO
    time.sleep(1)
    speak("I am Nana Banana. I am here to help you through this.")
    type_writer("    I am Nana Banana. I am here to help you through this.")
    time.sleep(1)
    
    # 1. THE NAME
    speak("Who are we honoring today?")
    type_writer("\n    Who are we honoring today?")
    name = input("       > ").strip()
    if not name: name = "Beloved"
    
    # 2. THE FILES
    speak(f"Okay. I will help you build a tribute for {name}.")
    time.sleep(0.5)
    speak("Please drag the folder containing her photos into this window.")
    type_writer("\n    [ACTION]: Drag the Photo Folder here and press Enter.")
    
    while True:
        folder_input = input("       > ")
        folder_path = Path(clean_path(folder_input))
        if folder_path.is_dir():
            images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png")) + list(folder_path.glob("*.jpeg")) + list(folder_path.glob("*.JPG"))
            if images:
                speak(f"I found {len(images)} memories.")
                type_writer(f"    >> Found {len(images)} photos.")
                break
            else:
                speak("That folder is empty. Please try another.")
                type_writer("    [!] No images found. Try again.")
        else:
            speak("I cannot read that folder. Please try again.")
            type_writer("    [!] Invalid folder path.")

    # 3. THE MUSIC
    speak("Now, what song should I weave into these memories?")
    type_writer("\n    [CONTEXT]: Type the Song and Artist (e.g., Luther Vandross).")
    song_query = input("       > ").strip()
    
    # FETCHING
    audio_path = fetch_song_cli(song_query)
    if not audio_path:
        speak("I failed to find that music. We will proceed in silence.")
        audio_path = None # Handle silent logic if needed, though fetch usually works
        sys.exit(1) # For now, let's stop if music fails, as music is key.

    # 4. THE PROCESSING
    speak(f"I am starting now. I will create {len(images)} videos.")
    type_writer(f"\n    [STATUS]: Rendering Tribute for {name}...")
    
    # Create Output Directory on Desktop
    desktop = Path(os.path.expanduser("~/Desktop"))
    output_dir = desktop / f"Tribute_for_{name.replace(' ', '_')}"
    output_dir.mkdir(exist_ok=True)
    
    success_count = 0
    for i, img in enumerate(images):
        if render_tribute(img, audio_path, output_dir, i+1, len(images)):
            success_count += 1
            
    # CLEANUP
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # CONCLUSION
    print("\n" + "="*60)
    speak("It is finished.")
    type_writer("    It is finished.")
    
    speak(f"I have placed the folder on your Desktop.")
    type_writer(f"    [LOCATION]: {output_dir}")
    
    speak("Would you like me to open it?")
    type_writer("\n    Open folder? (y/n)")
    if input("       > ").lower().startswith('y'):
        subprocess.run(['open', str(output_dir)])
        
    speak("I am still here. Peace.")
    type_writer("\n    [SESSION ENDED]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n    [Aborted]")
        sys.exit(0)
