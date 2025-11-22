#!/usr/bin/env python3
"""
StillHere API Server v2.2 - QuickTime Compatible
"""
from pathlib import Path
import tempfile
import logging
import subprocess
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response

# Mock core if missing
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

def convert_video(input_path, output_path, format_type="mp4"):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        shutil.copy(input_path, output_path)
        return

    cmd = [ffmpeg, '-y', '-i', str(input_path)]
    if format_type == "mov":
        # QuickTime Optimized
        cmd.extend(['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-f', 'mov'])
    else:
        # MP4 Universal
        cmd.extend(['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-movflags', '+faststart', '-f', 'mp4'])
    
    cmd.append(str(output_path))
    subprocess.run(cmd, check=True)

@app.post("/api/animate")
async def animate_endpoint(
    photo: UploadFile = File(...),
    style: str = Form("gentle_smile"), 
    duration: int = Form(5),           
    quality: str = Form("ultra"),
    format: str = Form("mp4"),
):
    tmp_dir = Path(tempfile.mkdtemp())
    photo_path = tmp_dir / photo.filename

    with photo_path.open("wb") as f:
        f.write(await photo.read())

    img = keeper.load_photo(str(photo_path))
    video_bytes = animator.animate(photo=img, style=style, duration=duration, quality=quality)

    # Save Raw
    raw_path = tmp_dir / "raw_output.mp4"
    keeper.save_memory(video_bytes, str(raw_path))

    # Convert
    ext = "mov" if format == "mov" else "mp4"
    final_path = tmp_dir / f"{photo.filename}_final.{ext}"
    
    convert_video(raw_path, final_path, format_type=format)

    with final_path.open("rb") as f:
        final_bytes = f.read()

    media_type = "video/quicktime" if format == "mov" else "video/mp4"
    return Response(content=final_bytes, media_type=media_type)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8282, reload=True)
