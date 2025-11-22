#!/usr/bin/env python3
"""
Create Funeral Avatar

One command. Shorty speaks at her own funeral.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from stillhere.core.lipsync import AvatarBuilder

def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "CREATING FUNERAL AVATAR" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Paths
    base_dir = Path(__file__).parent
    materials = base_dir / "funeral_materials" / "processed"
    
    # Find voice and photo
    voice_sample = materials / "VOICE_SAMPLE_FOR_AVATAR.wav"
    
    # Find best photo (any extension)
    photo = None
    for ext in ['.jpg', '.jpeg', '.png', '.heic']:
        candidate = materials / f"BEST_PHOTO_FOR_AVATAR{ext}"
        if candidate.exists():
            photo = candidate
            break
    
    if not voice_sample.exists():
        print("❌ No voice sample found")
        print("Run: python process_funeral_videos.py first")
        return
    
    if not photo:
        print("❌ No photo found")
        print("Run: python process_funeral_videos.py first")
        return
    
    print(f"Using:")
    print(f"  Voice: {voice_sample.name}")
    print(f"  Photo: {photo.name}")
    print()
    
    # The message - EDIT THIS
    message = """My beautiful family and friends,

I know you're hurting right now. I am too. 
But I want you to know something important - I'm still here.
I'm in every memory, every laugh, every moment we shared together.

Don't cry for too long. Live your lives. Love each other fiercely.
Take care of my grandbabies - they're everything to me.

I'll be watching over all of you, always.

This isn't goodbye. I'm just in a different place now.
Keep me in your hearts, and I'll never truly be gone.

I love you all so, so much.
"""
    
    print("Message she'll say:")
    print("-" * 70)
    print(message)
    print("-" * 70)
    print()
    
    response = input("Use this message? (yes/edit): ").strip().lower()
    
    if response == 'edit':
        print("\nEdit the message in this file:")
        print(f"  {__file__}")
        print("Look for the 'message =' section")
        print("\nThen run this script again.")
        return
    
    # Output
    output_video = base_dir / "FUNERAL_AVATAR_FINAL.mp4"
    
    print()
    print("Creating avatar...")
    print("This will take 5-10 minutes...")
    print()
    
    # Build avatar
    builder = AvatarBuilder()
    
    try:
        result = builder.create_speaking_avatar(
            photo_path=photo,
            voice_sample_path=voice_sample,
            text_to_speak=message,
            output_path=output_video,
            language="en"
        )
        
        print()
        print("=" * 70)
        print("✅ FUNERAL AVATAR COMPLETE")
        print("=" * 70)
        print()
        print(f"Video: {result}")
        print()
        print("To play at funeral:")
        print(f"  1. Copy {result.name} to USB drive")
        print(f"  2. Play on funeral home's system")
        print(f"  3. Or use your laptop")
        print()
        print("Shorty will speak. Everyone will feel her presence.")
        print()
        
    except Exception as e:
        print(f"\n❌ Error creating avatar: {e}\n")
        print("Make sure you have:")
        print("  pip install TTS soundfile")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped.\n")
    except Exception as e:
        print(f"\nError: {e}\n")
        import traceback
        traceback.print_exc()
