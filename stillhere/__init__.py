"""
StillHere - Bringing cherished memories to life through AI-powered photo animation.

Not a replacement for who we've lost.
A way to honor them. To remember them. To hold onto their presence.

Built with love for those who deserve to be remembered.
"""

__version__ = "0.1.0"
__author__ = "Everett Christman"

from stillhere.core.animator import Animator
from stillhere.core.restorer import Restorer
from stillhere.core.keeper import MemoryKeeper

__all__ = ["Animator", "Restorer", "MemoryKeeper"]
