import streamlit as st
import os
import subprocess
import shutil
from pathlib import Path
import time

# --- 0. SILENT CONFIG (No Nagging) ---
def silent_config():
    config_dir = Path(".streamlit")
    config_file = config_dir / "config.toml"
    if not config_dir.exists():
        config_dir.mkdir()
    if not config_file.exists() or "gatherUsageStats = false" not in config_file.read_text():
        with open(config_file, "w") as f:
            f.write("[browser]\ngatherUsageStats = false\n[server]\nheadless = false\n")
silent_config()

# --- 1. SANCTUARY CONFIGURATION ---
st.set_page_config(page_title="STILLHERE", page_icon="🕯️", layout="centered")

# --- 2. CATHEDRAL STYLING ---
st.markdown("""
    <style>
    /* THE VOID - Deep Dark Background */
    .stApp {
        background-color: #050505;
        color: #d4d4d4;
    }
    
    /* REMOVE DISTRACTIONS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* TYPOGRAPHY - Dignified */
    .title-text {
        font-family: 'Georgia', serif;
        font-size: 3.5em;
        text-align: center;
        color: #f0f0f0;
        margin-top: 20px;
        letter-spacing: 4px;
        text-shadow: 0px 0px 15px rgba(255,255,255,0.1);
    }
    
    .nana-speak {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 1.4em;
        font-weight: 300;
        text-align: center;
        color: #a8a8a8;
        margin-bottom: 40px;
        line-height: 1.6;
        padding: 20px;
        border-left: 1px solid #333;
        border-right: 1px solid #333;
    }
    
    /* INPUTS - Minimalist */
    .stTextInput>div>div>input {
        background-color: #111;
        color: #fff;
        border: none;
        border-bottom: 1px solid #444;
        text-align: center;
        font-size: 1.5em;
    }
    
    /* BUTTON - The Vigil */
    .stButton>button {
        background-color: #1a1a1a;
        color: #fff;
        border: 1px solid #333;
        border-radius: 2px;
        height: 60px;
        font-family: 'Georgia', serif;
        font-size: 1.2em;
        letter-spacing: 2px;
        margin-top: 30px;
    }
    .stButton>button:hover {
        background-color: #333;
        border-color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. EMPATHY ENGINE (Voice & Logic) ---

def speak(text):
    """Nana's Voice - Soft, Non-blocking"""
    # Using 'say' on Mac. -r 170 slows it down slightly for dignity.
    os.system(f"say -r 175 '{text}' &") 

def process_tribute(image_file, audio_path, output_folder, index):
    """
    The Engine: Fuses Photo + Music -> Apple ProRes .MOV
    """
    # 1. Temp Image Write
    temp_img_path = Path(f"temp_{index}_{image_file.name}")
    with open(temp_img_path, "wb") as f:
        f.write(image_file.getbuffer())

    # 2. Output Definition
    clean_name = Path(image_file.name).stem
    safe_name = f"{clean_name}_Tribute.mov"
    output_path = output_folder / safe_name
    
    # 3. Engine Check
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg and os.path.exists("/opt/homebrew/bin/ffmpeg"):
        ffmpeg = "/opt/homebrew/bin/ffmpeg"
    
    if not ffmpeg:
        return "MISSING_ENGINE"

    # 4. The Command (High Fidelity, No Shake)
    
    # Audio Logic
    if audio_path:
        # If song exists: Use it. Map video(0) and audio(1). 
        # Stop video when audio stops, OR stop at 30s (safeguard).
        inputs = ['-loop', '1', '-i', str(temp_img_path), '-i', str(audio_path)]
        maps = ['-map', '0:v', '-map', '1:a']
        # Force duration to length of song (or a safe cap if song is huge)
        # -shortest ensures video ends when audio ends
        duration = ['-shortest'] 
    else:
        # Silence (Vigil Mode)
        inputs = ['-loop', '1', '-i', str(temp_img_path), '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100']
        maps = ['-map', '0:v', '-map', '1:a']
        duration = ['-t', '10']

    # Filter: Scale to 1080p, keep format clean. NO ZOOM/SHAKE.
    # fade=in:0:30 = Fade in first 30 frames (1 sec) for softness.
    filter_complex = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fade=in:0:30"

    cmd = [
        ffmpeg, '-y',
        *inputs,
        '-vf', filter_complex,
        '-c:v', 'prores_ks', '-profile:v', '2', # ProRes Standard
        '-c:a', 'pcm_s16le',                    # Uncompressed Audio
        *maps,
        *duration,
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if temp_img_path.exists(): os.remove(temp_img_path)
        return str(output_path)
    except Exception as e:
        if temp_img_path.exists(): os.remove(temp_img_path)
        return f"ERROR: {str(e)}"

# --- 4. THE RITUAL (User Interface) ---

def main():
    # Session State for Voice
    if 'greeted' not in st.session_state:
        speak("I am here. The sanctuary is open.")
        st.session_state.greeted = True

    # Header
    st.markdown('<p class="title-text">STILLHERE</p>', unsafe_allow_html=True)
    
    # Agent Message
    st.markdown('<div class="nana-speak">"I am Nana Banana. I will help you honor <b>Sheila</b>. <br>Give me the photo. Give me the music. I will do the rest."</div>', unsafe_allow_html=True)

    # --- STEP 1: THE NAME ---
    # We assume Sheila, but allow edit if you want to add "Auntie" etc.
    name = st.text_input("WHO WE ARE HONORING", value="Sheila Ingram McNeil")

    # --- STEP 2: THE ARTIFACTS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 1. THE MEMORY (Photo)")
        uploaded_files = st.file_uploader("Upload Photo", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    with col2:
        st.markdown("#### 2. THE SOUNDTRACK (Music)")
        audio_file = st.file_uploader("Upload Song (MP3/WAV)", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

    # --- STEP 3: THE ACT ---
    st.markdown("---")
    
    if st.button("BEGIN THE TRIBUTE"):
        if not uploaded_files:
            st.error("Please provide a photo.")
            speak("I need the photo to begin.")
        elif not audio_file:
            # Allow proceed without audio? No, you asked for the soundtrack.
            st.warning("Please provide the song file (Luther Vandross).")
            speak("Please upload the song file.")
        else:
            # --- EXECUTION ---
            speak(f"Weaving the tribute for {name}. Please hold.")
            
            # Handle Audio File
            temp_audio_path = Path(f"temp_audio_{audio_file.name}")
            with open(temp_audio_path, "wb") as f:
                f.write(audio_file.getbuffer())
            
            # Output Folder (Desktop)
            desktop = Path(os.path.expanduser("~/Desktop"))
            memories_dir = desktop / f"Tribute_for_{name.replace(' ', '_')}"
            memories_dir.mkdir(exist_ok=True)
            
            progress_bar = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                result = process_tribute(uploaded_file, temp_audio_path, memories_dir, i)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
                
                if result and "ERROR" not in result and "MISSING" not in result:
                    st.success(f"✅ Preserved: {Path(result).name}")
                else:
                    st.error(f"Failed: {result}")

            # Cleanup Audio
            if temp_audio_path.exists():
                os.remove(temp_audio_path)
                
            speak("It is finished. I have opened the folder for you.")
            
            # Reveal
            subprocess.run(['open', str(memories_dir)])
            st.balloons()

if __name__ == "__main__":
    main()
