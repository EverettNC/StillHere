#!/usr/bin/env python3
"""
Family Upload Portal - For Shorty's Memorial
With Luther Vandross elegance and Shorty's presence
"""

import streamlit as st
from pathlib import Path
from datetime import datetime
import base64

st.set_page_config(
    page_title="Remembering Shorty",
    page_icon="🕊️",
    layout="centered"
)

# Function to load video
def get_video_base64(video_path):
    """Convert video to base64 for embedding."""
    with open(video_path, 'rb') as f:
        video_bytes = f.read()
    return base64.b64encode(video_bytes).decode()

# Elegant styling - Luther Vandross vibes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .main-header {
        text-align: center;
        color: #FFD700;
        font-family: 'Playfair Display', serif;
        font-size: 4em;
        font-weight: 700;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .sub-header {
        text-align: center;
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
        font-size: 1.5em;
        font-weight: 300;
        font-style: italic;
        margin-top: 0;
        margin-bottom: 30px;
    }
    
    .video-container {
        text-align: center;
        margin: 30px 0;
        border: 3px solid #FFD700;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
    }
    
    .arthur-message {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 35px;
        margin: 40px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    
    .arthur-text {
        color: #E8E8E8;
        font-family: 'Lato', sans-serif;
        font-size: 1.3em;
        line-height: 1.8;
        text-align: center;
    }
    
    .arthur-signature {
        color: #FFD700;
        font-family: 'Playfair Display', serif;
        font-size: 1.2em;
        text-align: right;
        margin-top: 20px;
        font-style: italic;
    }
    
    .upload-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 25px;
        margin: 25px 0;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    .section-title {
        color: #FFD700;
        font-family: 'Playfair Display', serif;
        font-size: 1.8em;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .footer {
        text-align: center;
        color: #888;
        font-family: 'Lato', sans-serif;
        margin-top: 60px;
        padding: 30px;
        font-size: 1.1em;
        font-style: italic;
    }
    
    .stFileUploader {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 20px;
    }
    
    .stFileUploader label {
        color: #E0E0E0 !important;
        font-family: 'Lato', sans-serif !important;
        font-size: 1.1em !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header - elegant like Luther
    st.markdown('<div class="main-header">Shorty</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">"One of the Best"</div>', unsafe_allow_html=True)
    
    # Shorty's video - her presence
    video_path = Path("/Users/EverettN/stillhere-work/static/shorty_memorial.mov")
    if video_path.exists():
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.video(str(video_path))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Arthur's message - warm and soulful
    st.markdown("""
    <div class="arthur-message">
        <div class="arthur-text">
            Hello, I'm Arthur.
            <br><br>
            Thank you for helping us honor Shorty's memory.
            <br><br>
            Every photo tells a story. Every video captures a moment.
            <br>
            Every memory you share helps keep her spirit alive.
            <br><br>
            Please take your time. Upload what speaks to your heart.
            <br><br>
            She was loved. She is remembered. She will never be forgotten.
        </div>
        <div class="arthur-signature">
            — Arthur
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create upload directory
    upload_dir = Path("/Users/EverettN/stillhere-work/funeral_materials")
    photos_dir = upload_dir / "photos"
    videos_dir = upload_dir / "videos"
    
    photos_dir.mkdir(parents=True, exist_ok=True)
    videos_dir.mkdir(parents=True, exist_ok=True)
    
    # Photos section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📷 Share Your Photos</div>', unsafe_allow_html=True)
    
    uploaded_photos = st.file_uploader(
        "Drag photos here, or click to browse",
        type=['jpg', 'jpeg', 'png', 'heic', 'heif'],
        accept_multiple_files=True,
        key="photos",
        label_visibility="visible"
    )
    
    if uploaded_photos:
        st.success(f"✨ {len(uploaded_photos)} photo(s) received with gratitude")
        
        # Save photos
        for photo in uploaded_photos:
            file_path = photos_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.name}"
            with open(file_path, 'wb') as f:
                f.write(photo.getbuffer())
        
        st.info("💙 Photos saved. Thank you for sharing these precious memories.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Videos section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎥 Share Your Videos</div>', unsafe_allow_html=True)
    
    uploaded_videos = st.file_uploader(
        "Drag videos here, or click to browse",
        type=['mp4', 'mov', 'avi', 'mkv', 'm4v'],
        accept_multiple_files=True,
        key="videos",
        label_visibility="visible"
    )
    
    if uploaded_videos:
        st.success(f"✨ {len(uploaded_videos)} video(s) received with gratitude")
        
        # Save videos
        for video in uploaded_videos:
            file_path = videos_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{video.name}"
            with open(file_path, 'wb') as f:
                f.write(video.getbuffer())
        
        st.info("💙 Videos saved. Thank you for sharing these precious moments.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer - Luther Vandross style
    st.markdown("""
    <div class="footer">
        "A house is not a home when there's no one there..."
        <br>
        But the love remains. Forever.
        <br><br>
        🕊️
        <br><br>
        With love,
        <br>
        The Family
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
