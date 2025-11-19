"""
Core modules for StillHere.

Contains the fundamental components:
- Animator: Photo animation engine
- Restorer: Photo enhancement and restoration
- MemoryKeeper: Encrypted storage for photos and videos
- Encryption: AES-256 encryption utilities
- Presence: Shared utilities (with Eruptor)
- Utils: Image/video processing utilities
"""

from stillhere.core.animator import Animator
from stillhere.core.restorer import Restorer
from stillhere.core.keeper import MemoryKeeper
from stillhere.core.encryption import Encryption
from stillhere.core.utils import ImageUtils, VideoUtils, FaceUtils

__all__ = ["Animator", "Restorer", "MemoryKeeper", "Encryption", "ImageUtils", "VideoUtils", "FaceUtils"]
