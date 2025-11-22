#!/usr/bin/env python3
"""
Arthur Web Interface

Family members click a link, upload photos/videos, Arthur does the rest.
No apps needed. Just a browser.
"""

import streamlit as st
from pathlib import Path
import shutil
from datetime import datetime
import json

st.set_page_config(
    page_title="StillHere - Arthur",
    page_icon="🕊️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF5F1F;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 1.2em;
        margin-top: 0;
    }
    .arthur-message {
        background: #1a1a1a;
        border-left: 4px solid #FF5F1F;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .step-header {
        color: #FF5F1F;
        font-size: 1.5em;
        border-bottom: 2px solid #FF5F1F;
        padding-bottom: 10px;
        margin: 30px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session():
    """Initialize session state."""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.session_dir = Path.home() / ".stillhere" / "web_sessions" / st.session_state.session_id
        st.session_state.session_dir.mkdir(parents=True, exist_ok=True)
        st.session_state.step = 'welcome'
        st.session_state.mode = None
        st.session_state.photos = []
        st.session_state.voice = None

def arthur_says(message):
    """Display Arthur's message."""
    st.markdown(f'<div class="arthur-message">🤖 <strong>Arthur:</strong> {message}</div>', unsafe_allow_html=True)

def main():
    init_session()
    
    # Header
    st.markdown('<div class="main-header">STILLHERE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">with Arthur, your guide</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Welcome
    if st.session_state.step == 'welcome':
        show_welcome()
    
    # Choose mode
    elif st.session_state.step == 'choose_mode':
        show_mode_selection()
    
    # Upload photos
    elif st.session_state.step == 'upload_photos':
        show_photo_upload()
    
    # Upload voice (Mode 3 only)
    elif st.session_state.step == 'upload_voice':
        show_voice_upload()
    
    # Enter message (Mode 3 only)
    elif st.session_state.step == 'enter_message':
        show_message_input()
    
    # Processing
    elif st.session_state.step == 'processing':
        show_processing()
    
    # Complete
    elif st.session_state.step == 'complete':
        show_complete()

def show_welcome():
    """Welcome screen."""
    st.markdown("## ")
    
    arthur_says(
        """Hello, I'm Arthur.
        
I'm here to help you honor someone you love.

This journey can be emotional, and that's okay. I'll guide you through everything, step by step. We'll go at your pace.

Just relax, and let me help you create something beautiful to remember them by."""
    )
    
    st.markdown("## ")
    
    if st.button("Let's Begin", type="primary", use_container_width=True):
        st.session_state.step = 'choose_mode'
        st.rerun()

def show_mode_selection():
    """Mode selection."""
    st.markdown('<div class="step-header">Step 1: Choose Your Memorial Experience</div>', unsafe_allow_html=True)
    
    arthur_says("I can help you create three different types of memorial videos. Choose the one that feels right:")
    
    st.markdown("## ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎬 Animated Photos")
        st.markdown("""
        **FREE**
        
        Your photos come to life with gentle motion.
        
        Perfect for: Slideshows, tributes
        
        Time: ~10 seconds
        """)
        if st.button("Choose Mode 1", key="mode1", use_container_width=True):
            st.session_state.mode = 'animated_photos'
            st.session_state.step = 'upload_photos'
            st.rerun()
    
    with col2:
        st.markdown("### 🎵 Photos + Music")
        st.markdown("""
        **$9.99**
        
        Animated photos set to meaningful music.
        
        Perfect for: Celebrations of life
        
        Time: ~10 seconds
        """)
        if st.button("Choose Mode 2", key="mode2", use_container_width=True):
            st.session_state.mode = 'photos_with_music'
            st.session_state.step = 'upload_photos'
            st.rerun()
    
    with col3:
        st.markdown("### 🗣️ Speaking Avatar")
        st.markdown("""
        **$29.99**
        
        Their photo speaks with their own voice.
        
        Perfect for: Final messages
        
        Time: 30-90 seconds
        """)
        if st.button("Choose Mode 3", key="mode3", use_container_width=True):
            st.session_state.mode = 'speaking_avatar'
            st.session_state.step = 'upload_photos'
            st.rerun()

def show_photo_upload():
    """Photo upload."""
    st.markdown('<div class="step-header">Step 2: Share Photos</div>', unsafe_allow_html=True)
    
    arthur_says("""I need photos of your loved one to create the video.

**What makes a good photo?**
- Clear face visible
- Good lighting  
- A photo you love
- High resolution if possible

You can upload multiple photos and I'll pick the best one.""")
    
    st.markdown("## ")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Drag and drop photos here, or click to browse",
        type=['jpg', 'jpeg', 'png', 'heic'],
        accept_multiple_files=True,
        key="photo_uploader"
    )
    
    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} photo(s) uploaded")
        
        # Save files
        photos_dir = st.session_state.session_dir / 'photos'
        photos_dir.mkdir(exist_ok=True)
        
        saved_photos = []
        for uploaded_file in uploaded_files:
            file_path = photos_dir / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            saved_photos.append(file_path)
        
        st.session_state.photos = saved_photos
        
        # Show previews
        st.markdown("### Your Photos:")
        cols = st.columns(min(len(uploaded_files), 3))
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i % 3]:
                st.image(uploaded_file, use_container_width=True)
        
        st.markdown("## ")
        
        if st.button("Continue", type="primary", use_container_width=True):
            if st.session_state.mode == 'speaking_avatar':
                st.session_state.step = 'upload_voice'
            else:
                st.session_state.step = 'processing'
            st.rerun()

def show_voice_upload():
    """Voice upload for Mode 3."""
    st.markdown('<div class="step-header">Step 3: Voice Sample</div>', unsafe_allow_html=True)
    
    arthur_says("""For a speaking avatar, I need a recording of their voice.

**This can be:**
- A video where they're talking
- A voice memo
- A phone call recording  
- Any audio of them speaking naturally

**Ideal length:** 10-30 seconds""")
    
    st.markdown("## ")
    
    uploaded_voice = st.file_uploader(
        "Upload voice/video file",
        type=['wav', 'mp3', 'm4a', 'mp4', 'mov'],
        key="voice_uploader"
    )
    
    if uploaded_voice:
        st.success(f"✓ Voice file uploaded: {uploaded_voice.name}")
        
        # Save file
        voice_dir = st.session_state.session_dir / 'voice'
        voice_dir.mkdir(exist_ok=True)
        
        voice_path = voice_dir / uploaded_voice.name
        with open(voice_path, 'wb') as f:
            f.write(uploaded_voice.getbuffer())
        
        st.session_state.voice = voice_path
        
        st.markdown("## ")
        
        if st.button("Continue", type="primary", use_container_width=True):
            st.session_state.step = 'enter_message'
            st.rerun()
    
    st.markdown("---")
    if st.button("Skip (use text-to-speech instead)", use_container_width=True):
        st.session_state.step = 'enter_message'
        st.rerun()

def show_message_input():
    """Message input for Mode 3."""
    st.markdown('<div class="step-header">Step 4: The Message</div>', unsafe_allow_html=True)
    
    arthur_says("""What would you like them to say?

This could be a final message to family, words of comfort, their favorite saying, or anything you wish they could say.""")
    
    st.markdown("## ")
    
    message = st.text_area(
        "Type the message:",
        height=200,
        placeholder="I love you so much. I'm always with you...",
        key="message_input"
    )
    
    if message:
        st.info(f"Message length: ~{len(message.split())} words (~{len(message.split()) * 0.5:.0f} seconds of speech)")
    
    st.markdown("## ")
    
    if st.button("Create Avatar", type="primary", use_container_width=True, disabled=not message):
        st.session_state.message = message
        st.session_state.step = 'processing'
        st.rerun()

def show_processing():
    """Processing screen."""
    st.markdown('<div class="step-header">Creating Your Memorial Video</div>', unsafe_allow_html=True)
    
    arthur_says("I'm working on this now. This usually takes 5-15 minutes. Feel free to step away - I'll be here when you return.")
    
    st.markdown("## ")
    
    # Progress simulation
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    import time
    steps = []
    
    if st.session_state.mode == 'animated_photos':
        steps = [
            "Selecting best photo...",
            "Adding gentle animation...",
            "Rendering video..."
        ]
    elif st.session_state.mode == 'photos_with_music':
        steps = [
            "Selecting best photo...",
            "Adding animation...",
            "Adding music...",
            "Rendering final video..."
        ]
    elif st.session_state.mode == 'speaking_avatar':
        steps = [
            "Processing voice sample...",
            "Cloning voice...",
            "Generating speech...",
            "Syncing lips to audio...",
            "Rendering final avatar..."
        ]
    
    for i, step in enumerate(steps):
        status_text.text(f"[{i+1}/{len(steps)}] {step}")
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(1)  # Simulate processing
    
    status_text.text("✓ Complete!")
    
    # TODO: Actually process the video here
    
    st.session_state.step = 'complete'
    time.sleep(1)
    st.rerun()

def show_complete():
    """Completion screen."""
    st.markdown('<div class="step-header">✅ Your Memorial Video Is Ready</div>', unsafe_allow_html=True)
    
    arthur_says("""Thank you for trusting me with this sacred task.

Your loved one's memory lives on in this video. Share it with those who need it.""")
    
    st.markdown("## ")
    
    # Download button (placeholder)
    st.download_button(
        label="📥 Download Your Video",
        data=b"",  # TODO: Actual video file
        file_name="memorial_video.mp4",
        mime="video/mp4",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown("## ")
    
    st.markdown("---")
    st.markdown("""
    **With compassion,**  
    Arthur
    
    ---
    
    *If you need to create another memorial video, refresh this page.*
    """)

if __name__ == "__main__":
    main()
