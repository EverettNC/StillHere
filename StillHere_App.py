import streamlit as st
import os
import time
import subprocess
import shutil
from pathlib import Path

# --- CONFIGURATION ---
st.set_page_config(page_title="StillHere Sanctuary", page_icon="🕯️", layout="wide")

# --- STYLING (THE CATHEDRAL) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e0e;
        color: #d4d4d4;
    }
    .header-text {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 3em;
        font-weight: 100;
        color: #f0f0f0;
        margin-bottom: 0px;
    }
    .agent-text {
        font-family: 'Georgia', serif;
        font-size: 1.2em;
        font-style: italic;
        color: #a8a8a8;
        border-left: 3px solid #ff4b4b;
        padding-left: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #1f1f1f;
        color: #ffffff;
        border: 1px solid #333;
        width: 100%;
        height: 60px;
        font-size: 1.2em;
    }
    .stButton>button:hover {
        border-color: #ffffff;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC: VOICE & PROCESSING ---

def speak(text):
    """Native Mac Voice - Non-blocking"""
    # We use '&' at the end of the command in shell so it doesn't freeze the UI
    os.system(f"say '{text}' &")

def process_memory(image_file, output_folder, song_name):
    """
    Takes the uploaded file object and turns it into a video using FFMPEG.
    """
    # 1. Save the uploaded file temporarily
    temp_path = Path("temp_upload.jpg")
    with open(temp_path, "wb") as f:
        f.write(image_file.getbuffer())

    # 2. Define Output
    safe_name = f"{image_file.name.split('.')[0]}_Memory.mov"
    output_path = output_folder / safe_name
    
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False

    # 3. FFMPEG Command (Zoom Effect + QuickTime Compatibility)
    cmd = [
        ffmpeg, '-y',
        '-loop', '1', '-i', str(temp_path),
        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-vf', "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1024x576,format=yuv420p",
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
        '-c:a', 'aac', '-b:a', '192k', '-t', '5',
        '-movflags', '+faststart',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return str(output_path)
    except Exception as e:
        return None

# --- THE APP UI ---

def main():
    # Session State for "Agent Memory"
    if 'greeted' not in st.session_state:
        speak("I am Nana Banana. Welcome to the Sanctuary. I am sorry for your loss.")
        st.session_state.greeted = True

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<p class="header-text">STILLHERE</p>', unsafe_allow_html=True)
    with col2:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/candle.png", width=60)

    # Agent Section
    st.markdown('<div class="agent-text">"I am here to handle the details. You just provide the memories." — Nana</div>', unsafe_allow_html=True)

    # Inputs
    st.markdown("### 1. Who are we honoring?")
    name = st.text_input("Name", placeholder="Sheila Ingram McNeil", label_visibility="collapsed")

    st.markdown("### 2. The Memories")
    uploaded_files = st.file_uploader("Drag and drop all your photos here at once.", 
                                      accept_multiple_files=True, 
                                      type=['png', 'jpg', 'jpeg'])

    st.markdown("### 3. The Atmosphere (Optional)")
    song = st.text_input("Song Context", placeholder="Luther Vandross")

    # The Trigger
    st.markdown("---")
    
    if st.button("Weave Memories"):
        if not uploaded_files:
            st.error("Please upload at least one photo.")
            speak("Please give me a photo to work with.")
        elif not name:
            st.error("Please enter a name.")
            speak("I need to know who we are honoring.")
        else:
            # START PROCESSING
            speak(f"I am beginning the work for {name}. Please wait.")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Create Folder
            memories_dir = Path("Memories")
            memories_dir.mkdir(exist_ok=True)
            
            processed_count = 0
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing: {uploaded_file.name}...")
                
                result_path = process_memory(uploaded_file, memories_dir, song)
                
                # Update Progress
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                
                if result_path:
                    processed_count += 1
            
            # COMPLETION
            status_text.text("Orchestration Complete.")
            st.success(f"Finished. {processed_count} memories have been created in the 'Memories' folder.")
            
            speak("It is finished. I have placed the videos in your folder.")
            
            # Open Folder Button
            if st.button("Open Folder"):
                subprocess.run(['open', str(memories_dir)])

if __name__ == "__main__":
    main()
