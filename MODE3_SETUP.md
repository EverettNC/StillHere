# Mode 3 Setup Guide: Speaking Avatar with Voice Cloning

**For honoring your aunt's memory with her authentic voice and presence.**

---

## What Mode 3 Does

Mode 3 creates complete speaking avatars:
1. **Voice Cloning** - Recreates your aunt's voice from audio samples
2. **Speech Generation** - Makes her say anything you write
3. **Lip Sync** - Realistic mouth movements matching the audio
4. **Animation** - Subtle life-like movements (breathing, blinking)

**Result**: A video where your aunt appears to be speaking naturally with her own voice.

---

## Installation

### Step 1: Install Dependencies

```bash
cd /Users/EverettN/stillhere-work

# Install voice cloning (TTS)
pip install TTS

# Install audio processing
pip install soundfile librosa pydub

# Install video processing (if not already installed)
pip install opencv-python imageio imageio-ffmpeg

# Verify FFmpeg is installed
ffmpeg -version
# If not installed: brew install ffmpeg (on Mac)
```

### Step 2: Test Voice Cloning

```python
from stillhere.core.voice import VoiceCloner

# Initialize
cloner = VoiceCloner()

# Test with a voice sample
cloner.clone_voice(
    text="Hello, this is a test of voice cloning",
    speaker_wav="path/to/voice_sample.wav",
    output_path="test_voice.wav"
)
```

### Step 3: Test Complete Avatar

```python
from stillhere.core.lipsync import AvatarBuilder

# Build avatar
builder = AvatarBuilder()

# Create speaking video
builder.create_speaking_avatar(
    photo_path="photo_of_aunt.jpg",
    voice_sample_path="aunt_voice_sample.wav",
    text_to_speak="I love you all so much. I'm always with you.",
    output_path="aunt_speaking.mp4"
)
```

---

## Voice Sample Requirements

### What Makes a Good Voice Sample?

✅ **Duration**: 5-30 seconds (ideal: 10-15 seconds)
✅ **Quality**: Clear audio, minimal background noise
✅ **Content**: Natural speech (not singing or shouting)
✅ **Speaker**: Only one person speaking
✅ **Format**: WAV, MP3, M4A, or FLAC

### How to Prepare Voice Samples

If you have recordings of your aunt:
1. **From videos**: Extract audio using ffmpeg
   ```bash
   ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 44100 aunt_voice.wav
   ```

2. **From voice memos**: Convert to WAV
   ```bash
   ffmpeg -i voice_memo.m4a aunt_voice.wav
   ```

3. **Clean up audio** (remove noise):
   - Use Audacity (free)
   - Apply: Effect > Noise Reduction
   - Apply: Effect > Normalize

### Multiple Samples (Recommended)

For best results, use 3-5 different voice samples:
- Different emotional tones
- Different contexts (phone calls, stories, laughter)
- Different times/settings

The system will blend them for a more authentic voice.

---

## Usage Examples

### Example 1: Simple Tribute Message

```python
from stillhere.core.lipsync import AvatarBuilder

builder = AvatarBuilder()

# Create 10-second tribute
builder.create_tribute_video(
    photo_path="aunt_favorite_photo.jpg",
    voice_sample_path="aunt_voice.wav",
    output_path="aunt_tribute.mp4",
    custom_message="I'm so proud of all of you. Keep loving each other."
)
```

### Example 2: Custom Message for Grandchildren

```python
# Message for college fund video
message = """
My beautiful grandchildren,
I want you to know how much I believe in you.
Education is the key to your dreams.
Work hard, be kind, and never give up.
I love you more than words can say.
"""

builder.create_speaking_avatar(
    photo_path="aunt_smiling.jpg",
    voice_sample_path="aunt_voice.wav",
    text_to_speak=message,
    output_path="aunt_college_message.mp4",
    language="en"
)
```

### Example 3: Multiple Videos (Batch Processing)

```python
from stillhere.core.voice import VoiceCloner

cloner = VoiceCloner()

messages = [
    "Happy birthday! I'm so proud of you.",
    "Congratulations on your graduation!",
    "I love you more than you'll ever know.",
    "Always remember: you are enough.",
    "Keep going. I'm with you every step."
]

# Generate all voice clips
voice_clips = cloner.batch_clone(
    texts=messages,
    speaker_wav="aunt_voice.wav",
    output_dir="aunt_messages",
    prefix="aunt_message"
)

# Create videos for each
for i, (voice_clip, message) in enumerate(zip(voice_clips, messages), 1):
    builder.create_speaking_avatar(
        photo_path="aunt_photo.jpg",
        voice_sample_path="aunt_voice.wav",  # Original sample
        text_to_speak=message,
        output_path=f"aunt_video_{i}.mp4"
    )
```

---

## Advanced Features

### Voice Library (Multiple People)

```python
from stillhere.core.voice import VoiceLibrary

# Create library
library = VoiceLibrary("family_voices")

# Add family members
library.add_voice_sample(
    name="Auntie_2023",
    audio_path="aunt_voice.wav",
    description="Aunt's voice from family gathering"
)

library.add_voice_sample(
    name="Auntie_2020_phone",
    audio_path="phone_call.wav",
    description="Phone call recording"
)

# List all profiles
profiles = library.list_profiles()
print(profiles)  # ['Auntie_2023', 'Auntie_2020_phone']

# Use a specific profile
aunt_voice = library.get_profile_audio("Auntie_2023")
```

### Quality Settings

```python
# High quality (slower, better results)
builder.create_speaking_avatar(
    photo_path="aunt.jpg",
    voice_sample_path="voice.wav",
    text_to_speak="Hello",
    output_path="high_quality.mp4",
    duration=10.0  # Exactly 10 seconds
)

# Fast preview (for testing)
from stillhere.core.lipsync import LipSyncer
syncer = LipSyncer()
syncer.sync_lips_to_audio(
    face_image="aunt.jpg",
    audio_file="pre_generated_voice.wav",
    output_path="preview.mp4",
    quality="low"  # Faster processing
)
```

### Languages

```python
# Get supported languages
from stillhere.core.voice import VoiceCloner
cloner = VoiceCloner()
languages = cloner.get_available_languages()
print(languages)

# Use different language
builder.create_speaking_avatar(
    photo_path="aunt.jpg",
    voice_sample_path="voice.wav",
    text_to_speak="Hola, te amo mucho.",
    output_path="spanish.mp4",
    language="es"  # Spanish
)
```

---

## Troubleshooting

### "TTS not installed"
```bash
pip install TTS
# If that fails:
pip install --upgrade pip
pip install TTS
```

### "FFmpeg not found"
```bash
# Mac:
brew install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### "Out of memory"
- Close other applications
- Use `quality="low"` for testing
- Process one video at a time
- Consider using CPU instead of GPU (slower but uses less memory)

### "Voice sounds robotic"
- Use longer voice sample (15-20 seconds ideal)
- Ensure voice sample is clear audio
- Try multiple voice samples
- Check that voice sample has natural speech patterns

### "Lips don't sync perfectly"
This is current limitation using FFmpeg fallback.
Full Wav2Lip integration coming soon for perfect lip sync.

---

## College Fund Integration (Future)

Mode 3 will be the premium tier:

**Free Tier** (Mode 1):
- Basic photo animation
- No voice

**Standard** (Mode 2):  
- Photo animation + music
- $9.99/video

**Premium** (Mode 3):
- Complete avatar with voice cloning
- $29.99/video
- Proceeds go to college fund

---

## Privacy & Storage

All voice cloning happens **locally** - no data sent to cloud.

To encrypt voice samples:
```python
from stillhere.core.keeper import MemoryKeeper

keeper = MemoryKeeper("encrypted_memories", passphrase="YourSecurePassphrase123")

# Store voice sample encrypted
keeper.save_photo(
    "aunt_voice.wav",
    tags=["voice", "aunt", "2023"],
    description="Aunt's voice sample"
)
```

---

## Next Steps

1. **Collect voice samples** - Gather audio of your aunt
2. **Choose best photo** - Clear face photo, good lighting
3. **Write message** - What should she say to her grandchildren?
4. **Generate tribute** - Create the speaking avatar
5. **Share with family** - Let them hear her voice again

**For your aunt. For her grandchildren. Forever.**

