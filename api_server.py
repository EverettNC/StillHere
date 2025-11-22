#!/usr/bin/env python3
"""
StillHere API Server v2.1
Optimized for High-Fidelity Memory Reconstruction & QuickTime Compatibility.
"""

from pathlib import Path
import tempfile
import logging
import subprocess
import shutil

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response

# Import Core Engines
try:
    from stillhere import Animator, MemoryKeeper
except ImportError:
    print("CRITICAL: 'stillhere' core package not found. Running in mock mode?")
    class Animator:
        def animate(self, **kwargs): return b"fake_video_bytes"
    class MemoryKeeper:
        def __init__(self, **kwargs): pass
        def load_photo(self, p): return p
        def save_memory(self, v, p): 
            with open(p, 'wb') as f: f.write(v)

app = FastAPI(
    title="StillHere High-Fidelity API",
    version="2.1.0",
    description="The engine behind the memories."
)

keeper = MemoryKeeper(encryption_passphrase="local-dev-passphrase") 
animator = Animator()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StillHere-API")

def convert_to_quicktime_safe(input_path, output_path):
    """
    Uses ffmpeg to ensure the video plays on Mac QuickTime.
    Requires 'ffmpeg' installed on the system.
    """
    ffmpeg_cmd = shutil.which("ffmpeg")
    if not ffmpeg_cmd:
        logger.warning("ffmpeg not found. Skipping conversion.")
        shutil.copy(input_path, output_path)
        return

    try:
        # Re-encode to H.264 (libx264) and AAC audio for max compatibility
        subprocess.run([
            ffmpeg_cmd, '-y',
            '-i', str(input_path),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart',
            str(output_path)
        ], check=True)
        logger.info("Converted video for QuickTime compatibility.")
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        # Fallback: just copy the original
        shutil.copy(input_path, output_path)

@app.post("/api/animate")
async def animate_endpoint(
    photo: UploadFile = File(...),
    style: str = Form("gentle_smile"), 
    duration: int = Form(5),           
    quality: str = Form("ultra"),      
):
    if not photo.filename:
        raise HTTPException(status_code=400, detail="Photo file must have a filename.")

    logger.info(f"Received request for: {photo.filename} | Style: {style}")

    tmp_dir = Path(tempfile.mkdtemp(prefix="stillhere_processing_"))
    photo_path = tmp_dir / photo.filename

    try:
        contents = await photo.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded photo is empty.")

        with photo_path.open("wb") as f:
            f.write(contents)

        img = keeper.load_photo(str(photo_path))

        # Execute Animation
        video_bytes = animator.animate(
            photo=img,
            style=style,
            duration=duration,
            quality=quality, 
        )

        # Save raw output
        raw_output_path = tmp_dir / "raw_output.mp4"
        keeper.save_memory(video_bytes, str(raw_output_path))

        # Convert for QuickTime
        final_output_path = tmp_dir / f"{photo.filename}_animated.mp4"
        convert_to_quicktime_safe(raw_output_path, final_output_path)

        if not final_output_path.exists():
            raise HTTPException(status_code=500, detail="Rendering failed.")

        with final_output_path.open("rb") as f:
            final_bytes = f.read()

        logger.info(f"Animation complete. Serving {len(final_bytes)} bytes.")
        return Response(content=final_bytes, media_type="video/mp4")

    except Exception as exc:
        logger.error(f"Animation Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8282, reload=True)
