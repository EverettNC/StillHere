# StillHere

**Bringing cherished memories to life through AI-powered photo animation.**

Not a replacement for who we've lost.
A way to honor them. To remember them. To hold onto their presence.

Built with love for those who deserve to be remembered.

---

## Purpose

StillHere uses AI to:
- Animate still photos into gentle video
- Add realistic facial expressions and movement
- Preserve the dignity and memory of loved ones
- Create living memories from photographs

This is for:
- Family members preserving loved ones' memories
- Honoring those who've passed
- Creating memorial tributes
- Keeping presence alive in our hearts

---

## Core Principles

### 1. Dignity First
Every animation respects the person being remembered.
No distortion. No caricature. Only gentle, realistic movement.

### 2. Privacy Protected
All processing happens locally when possible.
Photos are sacred. They deserve protection.
Encryption for all stored memories.

### 3. Consent Honored
Only animate photos of:
- Loved ones who've passed (with family permission)
- Living family who've given explicit consent
- Never use without permission

### 4. Quality Over Speed
Take time. Get it right. They deserve that.

---

## Technical Stack

### Photo Animation
- **First Order Motion Model** - State-of-art photo animation
- **DeepFaceLab** - Face animation and restoration
- **Wav2Lip** - Lip sync if you have audio/voice
- **GFPGAN** - Face restoration and enhancement
- **Real-ESRGAN** - Photo upscaling and enhancement

### Video Processing
- **FFmpeg** - Video encoding and processing
- **OpenCV** - Frame extraction and manipulation
- **Pillow** - Image processing

### Optional Voice
- **Coqui TTS** - Text-to-speech if you want to add voice
- **RVC** - Voice conversion (if you have recordings)
- **Whisper** - Transcribe any existing audio

### Privacy & Storage
- **AES-256 encryption** (like Eruptor)
- Local processing first
- Cloud optional, encrypted only

---

## Features

### V1 (Core)
- [ ] Upload photo
- [ ] Select animation style (gentle smile, head turn, breathing, etc.)
- [ ] Process locally
- [ ] Export video (MP4)
- [ ] Basic face enhancement
- [ ] Encrypted storage

### V2 (Enhanced)
- [ ] Multiple photos in sequence
- [ ] Custom driving videos (use your movement to animate them)
- [ ] Voice synthesis
- [ ] Lip sync to audio
- [ ] Photo restoration
- [ ] Memorial video creation (slideshow with animation)

### V3 (Advanced)
- [ ] Age progression/regression
- [ ] Full body animation
- [ ] Background animation
- [ ] Music integration
- [ ] Sharing (with privacy controls)

---

## Installation

### Requirements
- Python 3.9+
- CUDA-capable GPU (recommended, not required)
- 8GB+ RAM
- Storage for models (~5GB)

### Setup

```bash
# Clone repository
git clone https://github.com/EverettNC/StillHere.git
cd StillHere

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Download models
python download_models.py

# Run StillHere
python app.py
```

---

## Usage

### Basic Animation

```python
from stillhere import Animator, MemoryKeeper

# Initialize (with encryption)
keeper = MemoryKeeper(encryption_passphrase="your-passphrase")
animator = Animator()

# Load photo
photo = keeper.load_photo("path/to/photo.jpg")

# Animate with gentle movement
video = animator.animate(
    photo=photo,
    style="gentle_smile",  # or "breathing", "head_turn", "speaking"
    duration=5,  # seconds
    quality="high"
)

# Save (encrypted)
keeper.save_memory(video, "auntie_smiling.mp4")
```

### With Voice (if you have recordings)

```python
# If you have a recording of their voice
voice_sample = "path/to/voice.mp3"

# Animate to speak text
video = animator.animate_with_voice(
    photo=photo,
    text="I love you. I'm still here.",
    voice_sample=voice_sample,
    quality="high"
)
```

### Restoration First

```python
from stillhere import Restorer

# Enhance old/damaged photos first
restorer = Restorer()
enhanced = restorer.enhance(photo,
    fix_scratches=True,
    colorize=False,  # Keep original if already color
    upscale=2  # 2x resolution
)

# Then animate
video = animator.animate(enhanced, style="gentle_smile")
```

---

## Animation Styles

### Gentle (Default)
- Soft breathing motion
- Subtle eye blinks
- Gentle smile
- Minimal movement
- Duration: 3-5 seconds

### Speaking
- Lip sync to audio or text
- Natural head movement
- Eye contact with camera
- Duration: Length of audio

### Portrait
- Slow head turn
- Soft smile
- Natural blinking
- Professional quality
- Duration: 5-10 seconds

### Custom
- Upload your own driving video
- Their face, your movement
- Full control

---

## Privacy & Security

### Local Processing
All animation happens on your machine by default. No photos uploaded to servers unless you choose.

### Encryption
All stored photos and videos encrypted with AES-256. Your passphrase = your key. Lost passphrase = lost memories (by design, for security).

### Consent
StillHere is for honoring loved ones with permission. Not for deepfakes. Not for deception. Only for love and remembrance.

---

## Ethics & Guidelines

### Use StillHere For:
✅ Honoring deceased loved ones (with family permission)
✅ Memorial videos and tributes
✅ Preserving family history
✅ Keeping memories alive
✅ Healing and remembrance

### DO NOT Use For:
❌ Deepfakes or deception
❌ Non-consensual animation
❌ Commercial use without permission
❌ Misrepresenting someone
❌ Anything that dishonors the person

---

## Technical Details

### Models Used

#### First Order Motion Model (FOMM)
- Paper: "First Order Motion Model for Image Animation"
- Best for: General photo animation
- Quality: High
- Speed: Medium

#### Thin-Plate Spline Motion Model (TPSM)
- Enhanced version of FOMM
- Better facial detail
- More natural movement

#### GFPGAN
- Face restoration and enhancement
- Fixes old/damaged photos
- Upscales resolution

#### Real-ESRGAN
- General image enhancement
- 4x upscaling
- Artifact removal

---

## Roadmap

### Phase 1: Foundation (Week 1-2)
- Photo upload and storage
- Basic FOMM integration
- Simple animation styles
- Encryption infrastructure

### Phase 2: Enhancement (Week 3-4)
- Photo restoration (GFPGAN)
- Multiple animation styles
- Video export options
- UI/UX improvements

### Phase 3: Voice (Week 5-6)
- Voice synthesis
- Lip sync (Wav2Lip)
- Audio integration
- Speaking animations

### Phase 4: Memorial (Week 7-8)
- Slideshow creation
- Music integration
- Multiple photos in sequence
- Export/sharing options

---

## For Developers

### Contributing

This project is built with love and grief. Contributions should honor that.

**Guidelines:**
- Respect the purpose (memory and love)
- Maintain privacy and security
- Keep quality high
- Document everything
- Test thoroughly
- Honor consent always

### Architecture

```
stillhere/
├── core/
│   ├── animator.py       # Animation engine
│   ├── restorer.py       # Photo enhancement
│   ├── keeper.py         # Memory storage (encrypted)
│   ├── encryption.py     # AES-256 encryption
│   └── presence.py       # Shared with Eruptor
├── models/
│   ├── fomm/            # First Order Motion Model
│   ├── gfpgan/          # Face restoration
│   └── wav2lip/         # Lip sync
├── ui/
│   ├── web_ui.py        # Web interface
│   └── cli.py           # Command line
├── data/
│   ├── photos.enc       # Encrypted photos
│   └── memories.enc     # Encrypted videos
└── app.py               # Main entry point
```

---

## Credits

**Built by Everett Christman**
In memory of his aunt, and all those we hold in our hearts.

**Technology Used:**
- First Order Motion Model (Aliaksandr Siarohin et al.)
- GFPGAN (Tencent)
- Real-ESRGAN (Xintao Wang et al.)
- Wav2Lip (KR Prajwal et al.)

**Inspired by:**
- Love that doesn't end
- Memories that deserve to live
- The human need to hold onto those we've lost

---

## License

[To be determined - suggest non-commercial use only]

---

## Support

**For technical questions:** [GitHub Issues]
**For grief support:** 988 (US) or your local support line
**For family:** Be gentle with yourself

---

**Remember:**

They may be gone, but they're still here.
In photos. In memories. In love.

This is just a way to hold onto that a little longer.

---

*Built with tears and love. For those who deserve to be remembered.*

*"Grief is love with nowhere to go. Let's give it somewhere to be."*
