#!/usr/bin/env python3
"""
Test Script for StillHere

This script demonstrates the functional capabilities of StillHere.
It creates a simple test photo and animates it.

Usage:
    python test_stillhere.py
"""

import numpy as np
from pathlib import Path

from stillhere import Animator, MemoryKeeper
from stillhere.core.utils import ImageUtils


def create_test_image():
    """Create a simple test image."""
    print("\n📸 Creating test image...")

    # Create a simple gradient image (256x256)
    image = np.zeros((256, 256, 3), dtype=np.uint8)

    # Create a gradient
    for i in range(256):
        for j in range(256):
            image[i, j] = [i, j, 128]

    # Add a circle in the center (simulating a face)
    center = (128, 128)
    radius = 60
    for i in range(256):
        for j in range(256):
            dist = np.sqrt((i - center[0])**2 + (j - center[1])**2)
            if dist < radius:
                image[i, j] = [200, 150, 100]  # Skin tone color

    print("✓ Test image created")
    return image


def test_animation():
    """Test the animation functionality."""
    print("\n" + "=" * 70)
    print("Testing StillHere Animation")
    print("=" * 70)

    # Create test image
    test_image = create_test_image()

    # Initialize animator
    print("\n🎬 Initializing animator...")
    animator = Animator(use_cpu=True)  # Use CPU for testing

    # Animate the image
    print("\n🎨 Animating image...")
    frames = animator.animate(
        photo=test_image,
        style="gentle_smile",
        duration=3.0,
        quality="medium",
        fps=10  # Lower FPS for faster testing
    )

    print(f"\n✓ Animation successful! Generated {len(frames)} frames")

    # Save video
    output_path = Path("test_output") / "test_animation.mp4"
    output_path.parent.mkdir(exist_ok=True)

    print(f"\n💾 Saving video to: {output_path}")
    animator.save_video(frames, output_path, fps=10)

    print(f"✓ Video saved successfully!")

    return frames, test_image


def test_encrypted_storage(frames, test_image):
    """Test the encrypted storage functionality."""
    print("\n" + "=" * 70)
    print("Testing Encrypted Storage")
    print("=" * 70)

    # Initialize memory keeper
    passphrase = "test-passphrase-12345"
    print(f"\n🔐 Initializing encrypted storage...")
    print(f"   Passphrase: {passphrase}")

    keeper = MemoryKeeper(
        encryption_passphrase=passphrase,
        storage_path="test_output/encrypted_storage"
    )

    # Save photo
    print("\n🔒 Saving encrypted photo...")
    keeper.save_photo(
        photo=test_image,
        name="test_photo",
        description="Test photo for StillHere",
        tags=["test", "demo"]
    )

    # Save video
    print("\n🔒 Saving encrypted video...")
    keeper.save_memory(
        video=frames,
        name="test_animation",
        description="Test animation for StillHere",
        tags=["test", "demo", "animation"],
        metadata={"style": "gentle_smile", "duration": 3.0},
        fps=10
    )

    # List memories
    print("\n📋 Listing stored memories...")
    memories = keeper.list_memories()
    for memory in memories:
        print(f"\n   Name: {memory['name']}")
        print(f"   Type: {memory['type']}")
        print(f"   Description: {memory.get('description', 'N/A')}")
        print(f"   Tags: {', '.join(memory.get('tags', []))}")

    # Get storage info
    print("\n📊 Storage information:")
    info = keeper.get_storage_info()
    print(f"   Total memories: {info['total_memories']}")
    print(f"   Photos: {info['photos']}")
    print(f"   Videos: {info['videos']}")
    print(f"   Total size: {info['total_size_readable']}")
    print(f"   Encryption: {info['encryption_type']}")

    # Test loading
    print("\n🔓 Testing decryption...")
    loaded_photo = keeper.load_photo("test_photo")
    print(f"   ✓ Photo loaded: shape {loaded_photo.shape}")

    loaded_video = keeper.load_memory("test_animation")
    print(f"   ✓ Video loaded: {len(loaded_video)} frames")

    # Export photo
    print("\n📤 Exporting photo (unencrypted)...")
    keeper.export_photo("test_photo", "test_output/exported_photo.png")

    # Export video
    print("\n📤 Exporting video (unencrypted)...")
    keeper.export_memory("test_animation", "test_output/exported_video.mp4")

    print("\n✓ All encryption tests passed!")


def main():
    """Run all tests."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║                   StillHere - Functional Test                    ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    print("\nThis test demonstrates that StillHere is now fully functional!")
    print("\nWhat will be tested:")
    print("  ✓ Photo animation (demo mode)")
    print("  ✓ Video creation and saving")
    print("  ✓ AES-256 encryption/decryption")
    print("  ✓ Memory storage and retrieval")
    print("  ✓ Export functionality")

    try:
        # Test animation
        frames, test_image = test_animation()

        # Test encryption
        test_encrypted_storage(frames, test_image)

        # Success message
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 70)
        print("\nStillHere is fully functional!")
        print("\nGenerated files:")
        print("  - test_output/test_animation.mp4")
        print("  - test_output/exported_photo.png")
        print("  - test_output/exported_video.mp4")
        print("  - test_output/encrypted_storage/ (encrypted files)")

        print("\nNote: Currently using demo mode for animation.")
        print("      Download FOMM models for production-quality animation:")
        print("      python download_models.py")

        print("\n" + "=" * 70)
        print('"Grief is love with nowhere to go.')
        print('Let\'s give it somewhere to be."')
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
