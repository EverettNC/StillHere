import streamlit as st
import os
import subprocess
import shutil
from pathlib import Path
import yt_dlp # The new engine to fetch music

# --- 0. SILENT CONFIG ---
def silent_config():
    config_dir = Path(".streamlit")
    config_file = config_dir / "config.toml"
    if not config_dir.exists():
        config_dir.mkdir()
    if not config_file.exists() or "gatherUsageStats = false" not in config_file.read_text():
        with open(config_file, "w") as f:
            f.write("[browser]\ngatherUsageStats = false\n[server]\nheadless = false\n")
silent_config()

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="STILLHERE", page_icon="🕯️", layout="centered")

# --- 2. STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #d4d4d4; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .title-text { font-family: 'Georgia', serif; font-size: 3.5em; text-align: center; color: #f0f0f0; margin-top: 20px; letter-spacing: 4px; text-shadow: 0px 0px 15px rgba(255,255,255,0.1); }
    .nana-speak { font-family: 'Helvetica Neue', sans-serif; font-size: 1.4em; font-weight: 300; text-align: center; color: #a8a8a8; margin-bottom: 40px; padding: 20px; border-left: 1px solid #333; border-right: 1px solid #333; }
    .stTextInput>div>div>input { background-color: #111; color: #fff; border: none; border-bottom: 1px solid #444; text-align: center; font-size: 1.5em; }
    .stButton>button { background-color: #1a1a1a; color: #fff; border: 1px solid #333; height: 60px; font-family: 'Georgia', serif; font-size: 1.2em; letter-spacing: 2px; margin-top: 30px; }
    .stButton>button:hover { background-color: #333; border-color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---

def speak(text):
    os.system(f"say -r 175 '{text}' &")

def fetch_song(query):
    """
    Searches and downloads the song automatically.
    No user files required.
    """
    search_query = f"ytsearch1:{query} audio"
    temp_audio = "temp_downloaded_song"
    
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
            ydl.download([search_query])
        return f"{temp_audio}.mp3"
    except Exception as e:
        return None

def process_tribute(image_file, audio_path, output_folder, index):
    # 1. Temp Image
    temp_img_path = Path(f"temp_{index}_{image_file.name}")
    with open(temp_img_path, "wb") as f:
        f.write(image_file.getbuffer())

    # 2. Output
    clean_name = Path(image_file.name).stem
    safe_name = f"{clean_name}_Tribute.mov"
    output_path = output_folder / safe_name
    
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg and os.path.exists("/opt/homebrew/bin/ffmpeg"):
        ffmpeg = "/opt/homebrew/bin/ffmpeg"
    if not ffmpeg:
        return "MISSING_ENGINE"

    # 3. The Command
    # Loop image + Audio input
    inputs = ['-loop', '1', '-i', str(temp_img_path), '-i', str(audio_path)]
    
    # Filter: Scale 1080p, Fade in
    filter_complex = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fade=in:0:30"

    cmd = [
        ffmpeg, '-y',
        *inputs,
        '-vf', filter_complex,
        '-c:v', 'prores_ks', '-profile:v', '2',
        '-c:a', 'pcm_s16le',
        '-map', '0:v', '-map', '1:a',
        '-shortest', # Cut video when song ends
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if temp_img_path.exists(): os.remove(temp_img_path)
        return str(output_path)
    except Exception as e:
        if temp_img_path.exists(): os.remove(temp_img_path)
        return f"ERROR: {str(e)}"

# --- 4. INTERFACE ---

def main():
    if 'greeted' not in st.session_state:
        speak("I am here. Just tell me the song name.")
        st.session_state.greeted = True

    st.markdown('<p class="title-text">STILLHERE</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="nana-speak">"I will find the music. You just provide the memory."</div>', unsafe_allow_html=True)

    # --- INPUTS ---
    name = st.text_input("HONORING", value="Sheila Ingram McNeil")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. THE MEMORY")
        uploaded_files = st.file_uploader("Upload Photo", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    with col2:
        st.markdown("#### 2. THE SONG")
        # TEXT INPUT - NO FILE UPLOAD
        song_query = st.text_input("Type Song Name", placeholder="e.g. Luther Vandross Dance With My Father", label_visibility="collapsed")

    st.markdown("---")
    
    if st.button("BEGIN THE TRIBUTE"):
        if not uploaded_files:
            st.error("Please provide a photo.")
            speak("I need the photo.")
        elif not song_query:
            st.error("Please type a song name.")
            speak("What song should I find?")
        else:
            # --- FETCHING SONG ---
            speak(f"Searching for {song_query}...")
            with st.spinner(f"Retrieving '{song_query}' audio..."):
                audio_path = fetch_song(song_query)
            
            if not audio_path or not os.path.exists(audio_path):
                st.error("I could not download that song. Please try a simpler name.")
                speak("I could not find that song.")
                return

            # --- PROCESSING ---
            speak(f"I have the music. Weaving the tribute now.")
            
            desktop = Path(os.path.expanduser("~/Desktop"))
            memories_dir = desktop / f"Tribute_for_{name.replace(' ', '_')}"
            memories_dir.mkdir(exist_ok=True)
            
            progress_bar = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                result = process_tribute(uploaded_file, audio_path, memories_dir, i)
                progress_bar.progress((i + 1) / len(uploaded_files))
                
                if result and "ERROR" not in result:
                    st.success(f"✅ Preserved: {Path(result).name}")
                else:
                    st.error(f"Failed: {result}")

            # Cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)
                
            speak("It is finished. I have opened the folder.")
            subprocess.run(['open', str(memories_dir)])
            st.balloons()

if __name__ == "__main__":
    main()
