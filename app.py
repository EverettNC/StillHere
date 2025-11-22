import streamlit as st
import os
import subprocess
import shutil
from pathlib import Path

# --- 0. IMMEDIATE SETUP (Stop Streamlit Nagging) ---
# This block runs before the UI loads to ensure no email prompts appear.
def silent_config():
    config_dir = Path(".streamlit")
    config_file = config_dir / "config.toml"
    if not config_dir.exists():
        config_dir.mkdir()
    
    # If config is missing or doesn't have the email blocker, write it.
    if not config_file.exists() or "gatherUsageStats = false" not in config_file.read_text():
        content = """
[browser]
gatherUsageStats = false
[server]
headless = false
"""
        with open(config_file, "w") as f:
            f.write(content)

silent_config()

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="StillHere Sanctuary", page_icon="🕯️", layout="wide")

# --- 2. STYLING (The Sanctuary) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e0e;
        color: #d4d4d4;
    }
    /* Clean UI: Hide Hamburger menu and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Typography */
    .header-text {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 3em;
        font-weight: 100;
        color: #f0f0f0;
        margin-bottom: 0px;
    }
    .sub-header {
        font-family: 'Georgia', serif;
        font-size: 1.1em;
        color: #888;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .agent-text {
        font-family: 'Georgia', serif;
        font-size: 1.2em;
        font-style: italic;
        color: #a8a8a8;
        border-left: 3px solid #ff4b4b; /* Red Line of Presence */
        padding-left: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    /* Input Field Styling */
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #1f1f1f;
        color: #ffffff;
        border: 1px solid #333;
        width: 100%;
        height: 60px;
        font-size: 1.2em;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #ffffff;
        background-color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC (Direct & Voice) ---

def speak(text):
    """Native Mac Voice - Non-blocking (Background Process)"""
    # Uses 'say' to speak without freezing the app
    os.system(f"say '{text}' &")

def process_memory(image_file, output_folder):
    """
    Takes the uploaded file object and turns it into an Apple ProRes .MOV
    Using DIRECT FFMPEG (Bypassing the API Server for reliability).
    """
    # Save the uploaded file temporarily so FFMPEG can read it
    temp_path = Path(f"temp_{image_file.name}")
    with open(temp_path, "wb") as f:
        f.write(image_file.getbuffer())

    # Define Output Path
    clean_name = Path(image_file.name).stem
    safe_name = f"{clean_name}_Memory.mov"
    output_path = output_folder / safe_name
    
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return "NO_FFMPEG"

    # FFMPEG Command: Apple ProRes 422
    # This is the standard for Mac/QuickTime. It WILL play.
    cmd = [
        ffmpeg, '-y',
        '-loop', '1', '-i', str(temp_path), # Loop image
        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100', # Silent Audio
        # Zoom Effect: Slowly zooms in (1.0 to 1.5) over 6 seconds
        '-vf', "zoompan=z='min(zoom+0.0015,1.5)':d=150:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
