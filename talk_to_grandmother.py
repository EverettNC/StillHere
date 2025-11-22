#!/usr/bin/env python3
"""
Talk to Grandmother

Simple script for the boys to talk to their grandmother.
Just run this and she's there.
"""

import sys
from pathlib import Path

# Add stillhere to path
sys.path.insert(0, str(Path(__file__).parent))

from stillhere.core.companion import create_grandmother_companion, CompanionSession

def main():
    print()
    print("═" * 70)
    print("                    TALK TO GRANDMOTHER")
    print("═" * 70)
    print()
    
    # TODO: Replace these with actual files
    # For now, this will use text-only mode
    
    VOICE_SAMPLE = None  # Path("path/to/grandmother_voice.wav")
    PHOTO = None  # Path("path/to/grandmother_photo.jpg")
    
    # Describe grandmother's personality
    ABOUT_GRANDMOTHER = """
She was warm, loving, and full of wisdom.
She always knew the right thing to say when you were struggling.
She loved telling stories about her childhood and family.
She was proud of her grandchildren no matter what.
She had a gentle sense of humor and a kind smile.
She believed in hard work, education, and family above all.
She left us too soon, but her love remains forever.
"""
    
    # Create companion
    grandmother = create_grandmother_companion(
        name="Grandmother",
        voice_sample=VOICE_SAMPLE,
        photo=PHOTO,
        about_her=ABOUT_GRANDMOTHER
    )
    
    print("Grandmother is ready to talk.")
    print()
    
    # Start session
    session = CompanionSession(grandmother)
    
    if VOICE_SAMPLE:
        print("Starting voice session...")
        print("(You type, she speaks)")
        session.start_voice_session()
    else:
        print("Starting text session...")
        print("(Voice sample not configured - text only for now)")
        session.start_text_session()
    
    print()
    print("═" * 70)
    print("             She loves you. She's always here.")
    print("═" * 70)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye. She loves you.\n")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("  pip install openai")
        print("  export OPENAI_API_KEY='your-key-here'")
        print()
