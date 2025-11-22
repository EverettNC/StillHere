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

# --- 2. STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #d4d4d4; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .header-text { font-family: 'Helvetica Neue', sans-serif; font-size: 3em; font-weight: 100; color: #f0f0f0; margin-bottom: 0px; }
    .agent-text { font-family: 'Georgia', serif; font-size: 1.2em; font-style: italic; color: #a8a8a8; border-left: 3px solid #ff4b4b; padding-left: 20px; margin-top: 20px; margin-bottom: 20px; }
    .stButton>button { background-color: #1f1f1f; color: #ffffff; border: 1px solid #333; width: 100%; height: 60px; font-size: 1.2em; }
    .stButton>button:hover { border-color: #ffffff; background-color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
def speak(text):
    os.system(f"say '{text}' &")

def process_memory(image_file, output_folder):
    # Save temp file
    temp_path = Path(f"temp_{image_file.name}")
    with open(temp_path, "wb") as f:
        f.write(image_file.getbuffer())

    # Output path
    clean_name = Path(image_file.name).stem
    safe_name = f"{clean_name}_Memory.mov"
    output_path = output_folder / safe_name
    
    # CRITICAL CHECK: FIND ENGINE
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        # Trying common homebrew path if not in PATH
        if os.path.exists("/opt/homebrew/bin/ffmpeg"):
            ffmpeg = "/opt/homebrew/bin/ffmpeg"
        elif os.path.exists("/usr/local/bin/ffmpeg"):
            ffmpeg = "/usr/local/bin/ffmpeg"
        else:
            return "MISSING_ENGINE"

    cmd = [
        ffmpeg, '-y',
        '-loop', '1', '-i', str(temp_path),
        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-vf', "zoompan=z='min(zoom+0.0015,1.5)':d=150:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
        '-c:v', 'prores_ks', '-profile:v', '2',
        '-c:a', 'pcm_s16le',
        '-t', '6',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(temp_path)
        return str(output_path)
    except Exception as e:
        if temp_path.exists(): os.remove(temp_path)
        return f"ERROR: {str(e)}"

# --- 4. INTERFACE ---
def main():
    if 'greeted' not in st.session_state:
        speak("I am checking the system now.")
        st.session_state.greeted = True

    # Header
    st.markdown('<p class="header-text">STILLHERE</p>', unsafe_allow_html=True)
    
    # ENGINE DIAGNOSTIC (Run immediately)
    if not shutil.which("ffmpeg"):
        st.error("⚠️ CRITICAL ERROR: The Video Engine (FFMPEG) is missing.")
        st.markdown("""
        **Nana Banana says:** "I cannot weave the video because the loom is missing."
        
        **THE FIX:**
        1. Open a new terminal.
        2. Type: `brew install ffmpeg`
        3. Hit Enter.
        4. Once it finishes, reload this page.
        """)
        speak("I am missing a critical part. Please read the red box.")
        st.stop() # Halt the app

    # If engine is found, proceed
    st.markdown('<div class="agent-text">"Engine Detected. System Green. Drag your photos below." — Nana</div>', unsafe_allow_html=True)

    # Inputs
    name = st.text_input("Honoring", placeholder="Sheila Ingram McNeil")
    uploaded_files = st.file_uploader("Memories", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    song = st.text_input("Context", placeholder="Luther Vandross")

    st.markdown("---")
    
    if st.button("Weave Memories"):
        if not uploaded_files or not name:
            st.error("I need a name and a photo.")
            speak("I need a name and a photo.")
        else:
            speak(f"Processing for {name}.")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # FORCE OUTPUT TO DESKTOP
            desktop = Path(os.path.expanduser("~/Desktop"))
            memories_dir = desktop / "Sheila_Memories"
            memories_dir.mkdir(exist_ok=True)
            
            successes = 0
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing: {uploaded_file.name}...")
                result = process_memory(uploaded_file, memories_dir)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
                
                if result and "ERROR" not in result and "MISSING" not in result:
                    successes += 1
                else:
                    st.error(f"Failed on {uploaded_file.name}: {result}")
            
            if successes > 0:
                st.success(f"✅ {successes} Memories saved to your DESKTOP in the folder 'Sheila_Memories'.")
                speak("I have placed the folder on your desktop.")
                subprocess.run(['open', str(memories_dir)])
            else:
                st.error("No memories were created. Check the errors above.")

if __name__ == "__main__":
    main()
