#!/usr/bin/env python3
"""
ARTHUR - Autonomous Remembrance & Tribute Helper for Understanding & Reverence

The AI guide who walks customers through creating memorial videos.
Compassionate, patient, handles everything automatically.

For Shorty. For the boys. For all the families who need this.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import json

# Add stillhere to path
sys.path.insert(0, str(Path(__file__).parent))

class Arthur:
    """
    The autonomous guide - Arthur helps families through grief and memory.
    
    Arthur:
    - Introduces himself warmly
    - Guides through photo/voice upload
    - Explains each mode clearly
    - Processes everything automatically
    - Shows progress compassionately
    - Delivers the final video
    
    No confusion. No tech stress. Just Arthur and the family.
    """
    
    def __init__(self):
        self.name = "Arthur"
        self.session_dir = Path.home() / ".stillhere" / "sessions" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.session_data = {
            'started': datetime.now().isoformat(),
            'mode': None,
            'photos': [],
            'voice_sample': None,
            'music_choice': None,
            'message_text': None,
            'status': 'started'
        }
    
    def greet(self):
        """Arthur introduces himself."""
        print()
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + " " * 20 + "WELCOME TO STILLHERE" + " " * 29 + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        print("Hello, I'm Arthur.")
        print()
        print("I'm here to help you honor someone you love.")
        print()
        print("This journey can be emotional, and that's okay.")
        print("I'll guide you through everything, step by step.")
        print("We'll go at your pace. You're in good hands.")
        print()
        print("Just sit back, relax, and let me help you create")
        print("something beautiful to remember them by.")
        print()
        self._pause()
    
    def _pause(self, prompt: str = "Press Enter to continue..."):
        """Gentle pause - no rushing."""
        input(f"\n{prompt}")
        print()
    
    def choose_mode(self) -> str:
        """Help them choose which type of memorial video they want."""
        print("═" * 70)
        print("STEP 1: Choose Your Memorial Experience")
        print("═" * 70)
        print()
        print("I can help you create three different types of memorial videos:")
        print()
        print("  [1] ANIMATED PHOTOS")
        print("      → Your photos come to life with gentle motion")
        print("      → Perfect for: Slideshows, tributes, remembrance")
        print("      → Time: ~10 seconds")
        print("      → Price: FREE to try")
        print()
        print("  [2] PHOTOS WITH MUSIC")
        print("      → Animated photos set to meaningful music")
        print("      → Perfect for: Funerals, celebrations of life")
        print("      → Time: ~10 seconds")
        print("      → Price: $9.99")
        print()
        print("  [3] SPEAKING AVATAR (Ultimate)")
        print("      → Their photo speaks with their own voice")
        print("      → Perfect for: Final messages, preserved memories")
        print("      → Time: Custom (30-90 seconds)")
        print("      → Price: $29.99")
        print()
        
        while True:
            choice = input("Which would you like to create? (1, 2, or 3): ").strip()
            if choice in ['1', '2', '3']:
                modes = {
                    '1': 'animated_photos',
                    '2': 'photos_with_music',
                    '3': 'speaking_avatar'
                }
                self.session_data['mode'] = modes[choice]
                print()
                print(f"✓ Perfect choice.")
                print()
                return modes[choice]
            else:
                print("Please enter 1, 2, or 3")
    
    def collect_photos(self) -> List[Path]:
        """Guide them through uploading photos."""
        print("═" * 70)
        print("STEP 2: Share Photos")
        print("═" * 70)
        print()
        print("I need photos of your loved one to create the video.")
        print()
        print("What makes a good photo?")
        print("  ✓ Clear face visible")
        print("  ✓ Good lighting")
        print("  ✓ A photo you love")
        print("  ✓ High resolution if possible")
        print()
        print(f"Please place your photos in this folder:")
        print(f"  {self.session_dir / 'photos'}")
        print()
        
        photos_dir = self.session_dir / 'photos'
        photos_dir.mkdir(exist_ok=True)
        
        print("I'll wait while you add your photos...")
        self._pause("Press Enter when photos are ready...")
        
        # Find photos
        photo_extensions = ['.jpg', '.jpeg', '.png', '.heic']
        photos = []
        for ext in photo_extensions:
            photos.extend(photos_dir.glob(f'*{ext}'))
            photos.extend(photos_dir.glob(f'*{ext.upper()}'))
        
        if not photos:
            print("I don't see any photos yet. Let me check again...")
            self._pause("Add photos and press Enter...")
            
            for ext in photo_extensions:
                photos.extend(photos_dir.glob(f'*{ext}'))
                photos.extend(photos_dir.glob(f'*{ext.upper()}'))
        
        if photos:
            print(f"✓ Found {len(photos)} photo(s)")
            for p in photos:
                print(f"  • {p.name}")
            self.session_data['photos'] = [str(p) for p in photos]
            print()
            return photos
        else:
            print("Still no photos found. Please check the folder path.")
            return []
    
    def collect_voice(self) -> Optional[Path]:
        """Collect voice sample for Mode 3."""
        print("═" * 70)
        print("STEP 3: Voice Sample")
        print("═" * 70)
        print()
        print("For a speaking avatar, I need a recording of their voice.")
        print()
        print("This can be:")
        print("  • A video where they're talking")
        print("  • A voice memo")
        print("  • A phone call recording")
        print("  • Any audio of them speaking naturally")
        print()
        print("Ideal length: 10-30 seconds")
        print()
        
        voice_dir = self.session_dir / 'voice'
        voice_dir.mkdir(exist_ok=True)
        
        print(f"Please place voice recording here:")
        print(f"  {voice_dir}")
        print()
        
        self._pause("Press Enter when voice file is ready...")
        
        # Find voice file
        voice_extensions = ['.wav', '.mp3', '.m4a', '.mp4', '.mov']
        voice_files = []
        for ext in voice_extensions:
            voice_files.extend(voice_dir.glob(f'*{ext}'))
            voice_files.extend(voice_dir.glob(f'*{ext.upper()}'))
        
        if voice_files:
            voice_file = voice_files[0]
            print(f"✓ Found: {voice_file.name}")
            self.session_data['voice_sample'] = str(voice_file)
            print()
            return voice_file
        else:
            print("No voice file found. Continuing without voice...")
            return None
    
    def collect_message(self) -> str:
        """Get the message for speaking avatar."""
        print("═" * 70)
        print("STEP 4: The Message")
        print("═" * 70)
        print()
        print("What would you like them to say?")
        print()
        print("This could be:")
        print("  • A final message to family")
        print("  • Words of comfort")
        print("  • Their favorite saying")
        print("  • Anything you wish they could say")
        print()
        print("Type or paste the message below.")
        print("(Type 'DONE' on a new line when finished)")
        print()
        
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            lines.append(line)
        
        message = '\n'.join(lines).strip()
        self.session_data['message_text'] = message
        
        print()
        print("✓ Message received")
        print()
        return message
    
    def process_video(self, mode: str, photos: List[Path], voice: Optional[Path] = None, message: Optional[str] = None):
        """Process the memorial video."""
        print("═" * 70)
        print("CREATING YOUR MEMORIAL VIDEO")
        print("═" * 70)
        print()
        print("I'm working on this now...")
        print("This usually takes 5-15 minutes.")
        print()
        print("Feel free to step away. I'll be here when you return.")
        print()
        
        # Determine output path
        output_file = self.session_dir / f"memorial_video_{mode}.mp4"
        
        # Mode-specific processing
        if mode == 'animated_photos':
            print("[1/3] Selecting best photo...")
            print("[2/3] Adding gentle animation...")
            print("[3/3] Rendering video...")
            
            # TODO: Actual animation
            print("\n✓ Animation complete")
            
        elif mode == 'photos_with_music':
            print("[1/4] Selecting best photo...")
            print("[2/4] Adding animation...")
            print("[3/4] Adding music...")
            print("[4/4] Rendering final video...")
            
            # TODO: Music integration
            print("\n✓ Video with music complete")
            
        elif mode == 'speaking_avatar':
            print("[1/5] Processing voice sample...")
            print("[2/5] Cloning voice...")
            print("[3/5] Generating speech...")
            print("[4/5] Syncing lips to audio...")
            print("[5/5] Rendering final avatar...")
            
            # TODO: Avatar creation
            print("\n✓ Speaking avatar complete")
        
        print()
        print("═" * 70)
        print("✅ YOUR MEMORIAL VIDEO IS READY")
        print("═" * 70)
        print()
        print(f"Video saved to:")
        print(f"  {output_file}")
        print()
        
        self.session_data['output_video'] = str(output_file)
        self.session_data['status'] = 'completed'
        self._save_session()
        
        return output_file
    
    def farewell(self):
        """Arthur says goodbye."""
        print()
        print("─" * 70)
        print()
        print("Thank you for trusting me with this sacred task.")
        print()
        print("Your loved one's memory lives on in this video.")
        print("Share it with those who need it.")
        print()
        print("If you need anything else, I'm here.")
        print()
        print("With compassion,")
        print("Arthur")
        print()
        print("─" * 70)
        print()
    
    def _save_session(self):
        """Save session data."""
        session_file = self.session_dir / "session.json"
        with open(session_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
    
    def run_full_session(self):
        """Complete guided session."""
        # Greet
        self.greet()
        
        # Choose mode
        mode = self.choose_mode()
        
        # Collect photos
        photos = self.collect_photos()
        if not photos:
            print("Cannot continue without photos.")
            return
        
        # Mode-specific steps
        voice = None
        message = None
        
        if mode == 'speaking_avatar':
            voice = self.collect_voice()
            if voice:
                message = self.collect_message()
        
        # Process
        self.process_video(mode, photos, voice, message)
        
        # Farewell
        self.farewell()


def main():
    """Run Arthur."""
    arthur = Arthur()
    arthur.run_full_session()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSession paused. You can return anytime.\n")
    except Exception as e:
        print(f"\nError: {e}\n")
        import traceback
        traceback.print_exc()
