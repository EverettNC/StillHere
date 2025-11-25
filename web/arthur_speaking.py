"""
Arthur Speaking System
Makes Arthur actually TALK with voice + lip sync
Using StillHere core tech
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from stillhere.core.voice import VoiceSynthesizer
from stillhere.core.lipsync import LipSync
from stillhere.core.animator import Animator
import tempfile
import subprocess


class SpeakingArthur:
    """
    Arthur who actually SPEAKS with voice + animated face.
    Not just text - REAL talking avatar.
    """
    
    def __init__(self):
        self.voice = VoiceSynthesizer()
        self.lipsync = LipSync()
        self.animator = Animator()
        self.arthur_photo = Path(__file__).parent / 'static' / 'images' / 'Arthur.JPG'
        
    def speak(self, text: str, output_path: Path) -> Path:
        """
        Generate video of Arthur speaking the text.
        
        Returns path to video file.
        """
        # 1. Generate voice audio
        audio_path = self.voice.synthesize(
            text=text,
            voice='en-US-GuyNeural',  # Male voice for Arthur
            output_path=tempfile.mktemp(suffix='.wav')
        )
        
        # 2. Generate lip-synced video
        video_path = self.lipsync.sync_lips(
            photo=self.arthur_photo,
            audio=audio_path,
            output=output_path
        )
        
        return video_path
    
    def create_introduction_video(self) -> Path:
        """
        Create Arthur's auto-play introduction.
        
        "Hello, I'm Arthur. I know you're here because you've lost someone precious.
        I'm here to help you keep them close, forever. Let me guide you through this journey."
        """
        intro_text = """Hello, I'm Arthur.

I know you're here because you've lost someone precious.

I'm here to help you keep them close, forever.

Let me guide you through this journey together."""
        
        output_path = Path(__file__).parent / 'static' / 'videos' / 'arthur_intro.mp4'
        output_path.parent.mkdir(exist_ok=True)
        
        return self.speak(intro_text, output_path)


if __name__ == "__main__":
    # Generate Arthur's introduction video
    arthur = SpeakingArthur()
    video_path = arthur.create_introduction_video()
    print(f"Arthur introduction video created: {video_path}")
