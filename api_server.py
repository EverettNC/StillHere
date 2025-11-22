#!/usr/bin/env python3
"""
StillHere API Server v2.0
Optimized for High-Fidelity Memory Reconstruction.
"""

from pathlib import Path
import tempfile
import logging

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response

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
    version="2.0.0",
    description="The engine behind the memories."
)

keeper = MemoryKeeper(encryption_passphrase="local-dev-passphrase") 
animator = Animator()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StillHere-API")

@app.get("/health")
async def health():
    return {"status": "alive", "service": "stillhere-api", "mode": "high-fidelity"}

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

        # Execute Animation Pipeline with ULTRA quality
        video = animator.animate(
            photo=img,
            style=style,
            duration=duration,
            quality=quality, 
        )

        output_path = tmp_dir / f"{photo.filename}_animated.mp4"
        keeper.save_memory(video, str(output_path))

        if not output_path.exists():
            raise HTTPException(status_code=500, detail="Rendering failed.")

        with output_path.open("rb") as f:
            video_bytes = f.read()

        logger.info(f"Animation complete. Serving {len(video_bytes)} bytes.")
        return Response(content=video_bytes, media_type="video/mp4")

    except Exception as exc:
        logger.error(f"Animation Error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8282, reload=True)
