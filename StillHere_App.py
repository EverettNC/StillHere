import streamlit as st
import os
import subprocess
import shutil
from pathlib import Path

# --- 0. IMMEDIATE SETUP ---
def silent_config():
    config_dir = Path(".streamlit")
    config_file = config_dir / "config.toml"
    if not config_dir.exists():
        config_dir.mkdir()
    
    if not config_file.exists() or "gatherUsageStats = false" not in config_file.read_text():
        with open(config_file, "w") as f:
            f.write("[browser]\ngatherUsageStats = false\n[server]\nheadless = false\n")

silent_config()

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="StillHere Sanctuary", page_icon="🕯️", layout="wide")

# --- 2. STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #080808; color: #e0e0e0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .header-text { font-family: 'Helvetica Neue', sans-serif; font-size: 3em; font-weight: 100; color: #f0f0f0; margin-bottom: 0px; }
    .agent-text { font-family: 'Georgia', serif; font-size: 1.2em; font-style: italic; color: #a8a8a8; border-left: 3px solid #b30000; padding-left: 20px; margin-top: 20px; margin-bottom: 20px; }
    .stButton>button { background-color: #1a1a1a; color: #ffffff; border: 1px solid #444; width: 100%; height: 60px; font-size: 1.2em; }
    .stButton>button:hover { border-color: #ffffff; background-color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
def speak(text):
    os.system(f"say '{text}' &")

def process_memory(image_file, audio_path, output_folder):
    # 1. Save Image Temp
    temp_img_path = Path(f"temp_{image_file.name}")
    with open(temp_img_path, "wb") as f:
        f.write(image_file.getbuffer())

    # 2. Output Path
    clean_name = Path(image_file.name).stem
    safe_name = f"{clean_name}_Tribute.mov"
    output_path = output_folder / safe_name
    
    ffmpeg = shutil.which("ffmpeg")
    # Backup check for brew location
    if not ffmpeg and os.path.exists("/opt/homebrew/bin/ffmpeg"):
        ffmpeg = "/opt/homebrew/bin/ffmpeg"
        
    if not ffmpeg:
        return "MISSING_ENGINE"

    # 3. CONSTRUCT COMMAND (THE FIX)
    # If we have audio, use it. If not, silent.
    if audio_path:
        input_audio = ['-i', str(audio_path)]
        # Map audio from input #1 (the song)
        audio_map = ['-map', '0:v', '-map', '1:a']
        # Cut video to shortest input (stops when song stops or image duration)
        duration_flag = ['-t', '15'] # Default 15s if audio is long, or use -shortest
    else:
        input_audio = ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100']
        audio_map = []
        duration_flag = ['-t', '10']

    # VISUAL FIX: No more "Zoompan" shaking. 
    # Just a clean, high-quality static render that respects the photo.
    # We use scale to ensure even dimensions (prevent encoding errors).
    video_filter = "scale=1920:-2,format=yuv420p"

    cmd = [
        ffmpeg, '-y',
        '-loop', '1', '-i', str(temp_img_path),
        *input_audio,
        '-vf', video_filter,
        '-c:v', 'prores_ks', '-profile:v', '2', # Apple ProRes
        '-c:a', 'pcm_s16le', # Uncompressed Audio
        *duration_flag,
        *audio_map,
        '-shortest', # Stop when the shortest input ends
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(temp_img_path)
        return str(output_path)
    except Exception as e:
        if temp_img_path.exists(): os.remove(temp_img_path)
        return f"ERROR: {str(e)}"

# --- 4. INTERFACE ---
def main():
    if 'greeted' not in st.session_state:
        st.session_state.greeted = True

    # Header
    st.markdown('<p class="header-text">STILLHERE</p>', unsafe_allow_html=True)
    
    # Engine Check
    if not shutil.which("ffmpeg") and not os.path.exists("/opt/homebrew/bin/ffmpeg"):
        st.error("⚠️ CRITICAL: FFMPEG Engine is missing. Run 'brew install ffmpeg' in terminal.")
        st.stop()

    st.markdown('<div class="agent-text">"Upload the photo. Upload the song. I will combine them without distortion." — Nana</div>', unsafe_allow_html=True)

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 1. The Photo")
        uploaded_files = st.file_uploader("High Quality Photo", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    
    with col2:
        st.markdown("### 2. The Soundtrack")
        # THIS IS NEW: Actual File Upload for the music
        audio_file = st.file_uploader("Upload Song (MP3/WAV)", type=['mp3', 'wav', 'm4a'])

    st.markdown("---")
    
    if st.button("Weave Tribute"):
        if not uploaded_files:
            st.error("I need a photo.")
            speak("I need a photo.")
        else:
            speak("Orchestrating.")
            
            # Handle Audio
            temp_audio_path = None
            if audio_file:
                temp_audio_path = Path(f"temp_soundtrack{Path(audio_file.name).suffix}")
                with open(temp_audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())

            # Output Setup
            desktop = Path(os.path.expanduser("~/Desktop"))
            memories_dir = desktop / "Sheila_Memories"
            memories_dir.mkdir(exist_ok=True)
            
            progress_bar = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                result = process_memory(uploaded_file, temp_audio_path, memories_dir)
                progress_bar.progress((i + 1) / len(uploaded_files))
                
                if result and "ERROR" not in result:
                    st.success(f"✅ Saved: {Path(result).name}")
                else:
                    st.error(f"Failed: {result}")

            # Cleanup Audio
            if temp_audio_path and temp_audio_path.exists():
                os.remove(temp_audio_path)
            
            speak("The tribute is ready on your desktop.")
            subprocess.run(['open', str(memories_dir)])

if __name__ == "__main__":
    main()
