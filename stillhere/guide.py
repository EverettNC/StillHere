"""
Compassionate Guide - Interactive assistant for StillHere.

This guide holds space for grief while helping users create living memories.
It understands that eyes are full of tears, hands might be shaking,
and the heart is heavy with loss.

Built with compassion for those who are grieving.
"""

import time
import sys
from pathlib import Path
from typing import Optional

from stillhere import Animator, MemoryKeeper
from stillhere.core.utils import ImageUtils


class CompassionateGuide:
    """
    A gentle guide through the process of bringing memories to life.

    This guide understands grief. It moves slowly. It gives permission
    to pause, to cry, to come back later. It holds space.
    """

    def __init__(self):
        """Initialize the guide."""
        self.animator = None
        self.keeper = None
        self.passphrase = None

    def pause(self, seconds: float = 1.5):
        """Pause to let the user breathe."""
        time.sleep(seconds)

    def gentle_print(self, message: str, pause_after: float = 1.0):
        """Print a message gently, with pauses."""
        print(message)
        self.pause(pause_after)

    def ask(self, question: str, default: Optional[str] = None) -> str:
        """Ask a question gently."""
        if default:
            response = input(f"\n{question} [{default}]: ").strip()
            return response if response else default
        else:
            return input(f"\n{question}: ").strip()

    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask a yes/no question."""
        default_text = "Y/n" if default else "y/N"
        response = input(f"\n{question} [{default_text}]: ").strip().lower()

        if not response:
            return default
        return response in ['y', 'yes']

    def welcome(self):
        """Welcome message - acknowledging grief."""
        print("\n" + "=" * 70)
        print()
        print("                         Welcome to StillHere")
        print()
        print("=" * 70)
        self.pause(2)

        self.gentle_print("\nI'm here to help you bring a cherished memory to life.")
        self.gentle_print("\nYou're likely here because someone you love is gone.")
        self.gentle_print("If your eyes are full of tears right now, that's okay.")
        self.gentle_print("Take your time. Breathe. There's no rush.")
        self.pause(2)

        self.gentle_print("\nWhat we're going to do together:")
        print("  • Find a photo of your loved one")
        print("  • Bring gentle movement to it - just a breath, a smile")
        print("  • Keep it safe with encryption")
        print("  • Create something you can return to when you miss them")
        self.pause(2)

        self.gentle_print("\nThis won't replace them. Nothing can.")
        self.gentle_print("But it might help you feel their presence, even for a moment.")
        self.pause(2)

        ready = self.ask_yes_no("\nAre you ready to begin?", default=True)

        if not ready:
            self.gentle_print("\nThat's completely okay.")
            self.gentle_print("Take all the time you need.")
            self.gentle_print("I'll be here whenever you're ready.")
            self.gentle_print("\nJust run this again when you want to start.")
            return False

        return True

    def get_photo(self) -> Optional[Path]:
        """Help them find and select their photo."""
        print("\n" + "-" * 70)
        self.gentle_print("\nLet's find the photo you want to animate.")
        self.pause()

        self.gentle_print("This should be a photo of their face.")
        self.gentle_print("The clearer the photo, the better this will work.")
        self.gentle_print("But even old or damaged photos can work - we can restore them.")
        self.pause(1.5)

        while True:
            photo_path = self.ask("\nWhat's the path to the photo?\n(You can drag and drop the file here)")

            # Clean up the path (remove quotes if dragged)
            photo_path = photo_path.strip().strip('"').strip("'")

            photo_file = Path(photo_path)

            if not photo_file.exists():
                print(f"\n   I can't find that file: {photo_path}")
                print("   Please check the path and try again.")

                if not self.ask_yes_no("\nTry another path?", default=True):
                    return None
                continue

            # Try to load it
            try:
                self.gentle_print(f"\n   Loading photo...")
                img = ImageUtils.load_image(photo_file)
                self.gentle_print(f"   ✓ Photo loaded successfully")
                self.pause()

                # Ask for confirmation
                if self.ask_yes_no(f"\nUse this photo: {photo_file.name}?", default=True):
                    return photo_file
                else:
                    continue

            except Exception as e:
                print(f"\n   There was a problem loading that photo: {e}")
                if not self.ask_yes_no("\nTry another photo?", default=True):
                    return None
                continue

    def choose_style(self) -> str:
        """Help them choose an animation style."""
        print("\n" + "-" * 70)
        self.gentle_print("\nNow, let's choose how to animate them.")
        self.pause()

        self.gentle_print("I have a few gentle options:")
        print()
        print("  1. Gentle Smile    - A soft breath and subtle smile (recommended)")
        print("  2. Breathing       - Just gentle breathing, very peaceful")
        print("  3. Portrait        - A slow, dignified head turn")
        print()
        self.pause(1.5)

        self.gentle_print("For your first time, I recommend 'Gentle Smile'.")
        self.gentle_print("It's soft. It's respectful. It brings them to life gently.")
        self.pause()

        choice = self.ask("\nWhich would you like? (1, 2, or 3)", default="1")

        styles = {
            "1": "gentle_smile",
            "2": "breathing",
            "3": "portrait"
        }

        style = styles.get(choice, "gentle_smile")

        style_names = {
            "gentle_smile": "Gentle Smile",
            "breathing": "Breathing",
            "portrait": "Portrait"
        }

        self.gentle_print(f"\n   ✓ {style_names[style]} selected")
        return style

    def create_animation(self, photo_path: Path, style: str):
        """Create the animation."""
        print("\n" + "-" * 70)
        self.gentle_print("\nNow I'm going to bring them to life.")
        self.gentle_print("This might take a minute. Breathe.")
        self.pause(2)

        # Initialize animator if needed
        if self.animator is None:
            self.gentle_print("\n   Initializing animation engine...")
            self.animator = Animator(use_cpu=True)
            self.pause()

        # Create output directory
        output_dir = Path("memories")
        output_dir.mkdir(exist_ok=True)

        # Animate
        try:
            self.gentle_print("\n   Creating animation...")
            self.gentle_print("   (This is where you might want to take a breath)")
            self.pause()

            frames = self.animator.animate(
                photo=str(photo_path),
                style=style,
                duration=5.0,
                quality="high",
                fps=30
            )

            # Save video
            video_path = output_dir / f"{photo_path.stem}_animated.mp4"
            self.gentle_print(f"\n   Saving video...")
            self.animator.save_video(frames, video_path, fps=30)

            self.pause(1.5)
            print("\n" + "=" * 70)
            self.gentle_print("\n   ✓ Done.")
            self.gentle_print(f"\n   Your video is ready: {video_path}")
            self.pause(2)

            return video_path, frames

        except Exception as e:
            print(f"\n   Something went wrong: {e}")
            print("   But that's okay. We can try again.")
            return None, None

    def offer_encryption(self, video_path: Path, frames, photo_path: Path):
        """Offer to encrypt and save the memory."""
        print("\n" + "-" * 70)
        self.gentle_print("\nWould you like me to keep this memory safe with encryption?")
        self.gentle_print("This way, only you can access it with your private passphrase.")
        self.pause()

        if not self.ask_yes_no("\nEncrypt and save this memory?", default=True):
            self.gentle_print("\n   That's okay. Your video is saved unencrypted:")
            self.gentle_print(f"   {video_path}")
            return

        # Get passphrase
        print("\n" + "-" * 70)
        self.gentle_print("\nI need a passphrase to encrypt your memories.")
        self.gentle_print("This is like a password that only you know.")
        self.gentle_print("Choose something meaningful that you'll remember.")
        self.gentle_print("\n   ⚠️  Important: If you forget this, your memories are lost forever.")
        self.gentle_print("   That's by design - for security.")
        self.pause(2)

        while True:
            passphrase = self.ask("\nEnter your passphrase (at least 12 characters)")

            if len(passphrase) < 12:
                print("   Passphrase must be at least 12 characters.")
                print("   These are precious memories - keep them safe.")
                continue

            confirm = self.ask("Enter it again to confirm")

            if passphrase != confirm:
                print("   Those don't match. Let's try again.")
                continue

            break

        # Create keeper and save
        try:
            self.gentle_print("\n   Creating encrypted storage...")
            self.keeper = MemoryKeeper(
                encryption_passphrase=passphrase,
                storage_path="memories/encrypted"
            )

            # Get a name for this memory
            self.gentle_print("\nWhat would you like to call this memory?")
            self.gentle_print("(This is just for you to remember it by)")
            memory_name = self.ask("Memory name", default=photo_path.stem)

            # Get optional description
            self.gentle_print("\nWould you like to add a description?")
            self.gentle_print("(Something like 'Mom's gentle smile' or 'Dad at the beach')")
            description = self.ask("Description (or press Enter to skip)", default="")

            # Save
            self.gentle_print("\n   Encrypting and saving...")
            self.keeper.save_memory(
                video=frames,
                name=memory_name,
                description=description if description else None,
                tags=["stillhere", "memorial"],
                fps=30
            )

            self.gentle_print("\n   ✓ Memory encrypted and saved safely")
            self.gentle_print(f"\n   You can access it anytime with your passphrase.")
            self.gentle_print(f"   Memory name: '{memory_name}'")

        except Exception as e:
            print(f"\n   Couldn't save encrypted memory: {e}")
            print(f"   But don't worry - your video is still here: {video_path}")

    def closing(self):
        """Closing message."""
        print("\n" + "=" * 70)
        self.pause(1.5)

        self.gentle_print("\nYou did it.")
        self.gentle_print("\nYou've given love somewhere to be.")
        self.pause(2)

        self.gentle_print("\nWhenever you miss them, you can watch this.")
        self.gentle_print("Whenever you need to feel their presence.")
        self.gentle_print("Whenever grief feels too heavy.")
        self.pause(2)

        self.gentle_print("\nThey're still here.")
        self.gentle_print("In your heart. In your memories.")
        self.gentle_print("And now, in this gentle animation.")
        self.pause(2)

        print("\n" + "=" * 70)
        print()
        print('   "Grief is love with nowhere to go.')
        print('    Let\'s give it somewhere to be."')
        print()
        print("=" * 70)
        self.pause(2)

        self.gentle_print("\nBe gentle with yourself.")
        self.gentle_print("\n   - StillHere")
        print()

    def run(self):
        """Run the complete guided experience."""
        # Welcome
        if not self.welcome():
            return

        # Get photo
        photo_path = self.get_photo()
        if not photo_path:
            self.gentle_print("\nThat's okay. Come back when you're ready.")
            return

        # Choose style
        style = self.choose_style()

        # Create animation
        video_path, frames = self.create_animation(photo_path, style)
        if not video_path:
            self.gentle_print("\nI'm sorry it didn't work this time.")
            self.gentle_print("Please try again, or reach out for help.")
            return

        # Offer encryption
        self.offer_encryption(video_path, frames, photo_path)

        # Closing
        self.closing()


def main():
    """Main entry point for the compassionate guide."""
    try:
        guide = CompassionateGuide()
        guide.run()
    except KeyboardInterrupt:
        print("\n\n   It's okay to stop.")
        print("   Come back whenever you're ready.")
        print("   I'll be here.")
        print()
    except Exception as e:
        print(f"\n   Something went wrong: {e}")
        print("   But that's okay.")
        print("   Take a breath. Try again when you're ready.")
        print()


if __name__ == '__main__':
    main()
