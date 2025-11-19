#!/usr/bin/env python3
"""
StillHere - Example Usage

This example shows how to use StillHere to animate photos and preserve memories.

Note: This is the project foundation. The actual AI models will be integrated
in Phase 1-3. For now, this demonstrates the API design.
"""

from stillhere import Animator, Restorer, MemoryKeeper
from pathlib import Path


def example_basic_animation():
    """Example: Basic photo animation."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Photo Animation")
    print("=" * 70 + "\n")

    # Initialize animator
    animator = Animator()

    # Animate with gentle smile (the default, most respectful style)
    print("Animating photo with gentle smile...")
    video = animator.animate(
        photo="path/to/photo.jpg",  # Your photo path
        style="gentle_smile",
        duration=5,
        quality="high"
    )

    print("✓ Animation complete (placeholder - will work in Phase 1)")


def example_photo_restoration():
    """Example: Restore an old or damaged photo."""
    print("\n" + "=" * 70)
    print("Example 2: Photo Restoration")
    print("=" * 70 + "\n")

    # Initialize restorer
    restorer = Restorer()

    # Enhance old photo
    print("Restoring old photo...")
    enhanced = restorer.enhance(
        photo="path/to/old_photo.jpg",
        fix_scratches=True,
        upscale=2,
        quality="high"
    )

    print("✓ Restoration complete (placeholder - will work in Phase 2)")


def example_encrypted_storage():
    """Example: Store memories with encryption."""
    print("\n" + "=" * 70)
    print("Example 3: Encrypted Memory Storage")
    print("=" * 70 + "\n")

    # Initialize memory keeper with encryption
    keeper = MemoryKeeper(
        encryption_passphrase="my-secure-passphrase-at-least-12-chars"
    )

    # Save a photo (encrypted)
    print("Saving encrypted photo...")
    keeper.save_photo(
        photo="path/to/photo.jpg",
        name="aunt_mary",
        description="Aunt Mary, Christmas 1985",
        tags=["family", "christmas", "1985"]
    )

    # List all memories
    print("\nListing stored memories...")
    memories = keeper.list_memories()

    print("✓ Storage complete (placeholder - encryption works now!)")


def example_complete_workflow():
    """Example: Complete workflow - restore, animate, and save."""
    print("\n" + "=" * 70)
    print("Example 4: Complete Workflow")
    print("=" * 70 + "\n")

    # Step 1: Restore old photo
    print("Step 1: Restoring photo...")
    restorer = Restorer()
    enhanced = restorer.enhance(
        photo="path/to/old_photo.jpg",
        fix_scratches=True,
        upscale=2
    )

    # Step 2: Animate the enhanced photo
    print("Step 2: Animating enhanced photo...")
    animator = Animator()
    video = animator.animate(
        photo=enhanced,
        style="gentle_smile",
        duration=5,
        quality="high"
    )

    # Step 3: Save with encryption
    print("Step 3: Saving encrypted memory...")
    keeper = MemoryKeeper(encryption_passphrase="secure-passphrase")
    keeper.save_memory(
        video=video,
        name="aunt_mary_smiling",
        description="Aunt Mary's gentle smile",
        tags=["family", "restored"],
        metadata={
            "original_photo": "old_photo.jpg",
            "restoration": "enhanced",
            "animation_style": "gentle_smile"
        }
    )

    print("✓ Complete workflow finished (placeholder)")


def example_animation_styles():
    """Example: Different animation styles."""
    print("\n" + "=" * 70)
    print("Example 5: Different Animation Styles")
    print("=" * 70 + "\n")

    animator = Animator()

    # Get info about each style
    styles = ["gentle_smile", "breathing", "head_turn", "portrait"]

    for style in styles:
        info = animator.get_style_info(style)
        print(f"\n{info.get('name', style)}:")
        print(f"  Description: {info.get('description', 'N/A')}")
        print(f"  Duration: {info.get('duration', 'N/A')}")
        print(f"  Best for: {info.get('best_for', 'N/A')}")


def main():
    """Run all examples."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║                    StillHere - Examples                          ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    print("\nThese examples demonstrate the StillHere API.")
    print("Note: This is the project foundation. AI models will be added in Phase 1-3.")
    print("\nCurrently showing API design with placeholder implementations.")

    # Run examples
    example_basic_animation()
    example_photo_restoration()
    example_encrypted_storage()
    example_complete_workflow()
    example_animation_styles()

    print("\n" + "=" * 70)
    print("Examples Complete")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Download models: python download_models.py (Phase 1+)")
    print("3. Try the CLI: python app.py --cli --help")
    print("4. Or web UI: python app.py")
    print("\n" + "=" * 70)
    print('\n"Grief is love with nowhere to go.')
    print('Let\'s give it somewhere to be."')
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
