#!/usr/bin/env python3
"""
StillHere API Server v2.1 - QuickTime Compatible
"""

from pathlib import Path
import tempfile
import logging
import subprocess
import shutil

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response

# Import Core Engines (Mock if missing)
try:
    from stillhere import Animator, MemoryKeeper
except ImportError:
    class Animator:
        def animate(self, **kwargs): return b"fake_video_bytes"
    class MemoryKeeper:
        def __init__(self, **kwargs): pass
        def load_photo(self, p): return p
        def save_memory(self, v, p): 
            with open(p, 'wb') as f: f.write(v)

app = FastAPI(title="StillHere API")
keeper = MemoryKeeper(encryption_passphrase="local") 
animator = Animator()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StillHere-API")

def convert_to_quicktime(input_path, output_path):
    """Ensures video plays on Mac/QuickTime using ffmpeg."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        shutil.copy(input_path, output_path)
        return

    try:
        subprocess.run([
            ffmpeg, '-y', '-i', str(input_path),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart',
            str(output_path)
        ], check=True)
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        shutil.copy(input_path, output_path)

@app.post("/api/animate")
async def animate_endpoint(
    photo: UploadFile = File(...),
    style: str = Form("gentle_smile"), 
    duration: int = Form(5),           
    quality: str = Form("ultra"),      
):
    tmp_dir = Path(tempfile.mkdtemp())
    photo_path = tmp_dir / photo.filename

    # Save Input
    with photo_path.open("wb") as f:
        f.write(await photo.read())

    # Animate
    img = keeper.load_photo(str(photo_path))
    video_bytes = animator.animate(photo=img, style=style, duration=duration, quality=quality)

    # Save Raw
    raw_path = tmp_dir / "raw.mp4"
    keeper.save_memory(video_bytes, str(raw_path))

    # Convert for Mac
    final_path = tmp_dir / f"{photo.filename}_final.mp4"
    convert_to_quicktime(raw_path, final_path)

    # Serve
    with final_path.open("rb") as f:
        final_bytes = f.read()

    return Response(content=final_bytes, media_type="video/mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8282, reload=True)
