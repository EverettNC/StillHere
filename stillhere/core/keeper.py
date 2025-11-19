"""
MemoryKeeper - Encrypted storage for StillHere.

Photos are sacred. Memories are precious.
They deserve protection with military-grade encryption.

Uses AES-256 encryption (same as Eruptor) to keep your loved ones safe.
Your passphrase is the only key. Lose it, and the memories are gone forever.
This is by design. Security through privacy.
"""

from typing import Optional, Union, Dict, Any, List
from pathlib import Path
import json
from datetime import datetime
import numpy as np


class MemoryKeeper:
    """
    Encrypted storage manager for photos and videos.

    Keeps your memories safe with AES-256 encryption.

    Example:
        >>> keeper = MemoryKeeper(encryption_passphrase="your-secret-passphrase")
        >>> keeper.save_photo("photo.jpg", "aunt_mary.jpg")
        >>> photo = keeper.load_photo("aunt_mary.jpg")
    """

    def __init__(
        self,
        encryption_passphrase: str,
        storage_path: Optional[Union[str, Path]] = None
    ):
        """
        Initialize the MemoryKeeper.

        Args:
            encryption_passphrase: Passphrase for AES-256 encryption
            storage_path: Path to encrypted storage directory (default: ./data)

        Raises:
            ValueError: If passphrase is too weak
        """
        if len(encryption_passphrase) < 12:
            raise ValueError(
                "Passphrase must be at least 12 characters. "
                "These are your precious memories - keep them safe."
            )

        self.passphrase = encryption_passphrase
        self.storage_path = Path(storage_path) if storage_path else Path("data")
        self.storage_path.mkdir(exist_ok=True)

        # Initialize encryption
        from stillhere.core.encryption import Encryption
        self.encryption = Encryption(passphrase)

        # Metadata file (encrypted)
        self.metadata_file = self.storage_path / "memories_metadata.enc"
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load encrypted metadata about stored memories."""
        if not self.metadata_file.exists():
            return {}

        try:
            encrypted_data = self.metadata_file.read_bytes()
            decrypted_json = self.encryption.decrypt(encrypted_data)
            return json.loads(decrypted_json)
        except Exception as e:
            print(f"Warning: Could not load metadata: {e}")
            return {}

    def _save_metadata(self):
        """Save encrypted metadata."""
        try:
            json_data = json.dumps(self.metadata, indent=2)
            encrypted_data = self.encryption.encrypt(json_data.encode())
            self.metadata_file.write_bytes(encrypted_data)
        except Exception as e:
            print(f"Error saving metadata: {e}")

    def save_photo(
        self,
        photo: Union[str, Path, np.ndarray],
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Path:
        """
        Save a photo with encryption.

        Args:
            photo: Path to photo or numpy array
            name: Name for the stored photo
            description: Optional description of the photo
            tags: Optional tags for organization

        Returns:
            Path to encrypted photo file
        """
        # TODO: Implement photo encryption and storage
        print(f"Saving encrypted photo: {name}")

        # Store metadata
        self.metadata[name] = {
            "type": "photo",
            "description": description,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "original_name": str(photo) if isinstance(photo, (str, Path)) else "array"
        }
        self._save_metadata()

        # Placeholder return
        return self.storage_path / f"{name}.enc"

    def load_photo(
        self,
        name: str
    ) -> np.ndarray:
        """
        Load and decrypt a photo.

        Args:
            name: Name of the stored photo

        Returns:
            Photo as numpy array

        Raises:
            FileNotFoundError: If photo doesn't exist
            ValueError: If decryption fails (wrong passphrase)
        """
        # TODO: Implement photo decryption and loading
        print(f"Loading encrypted photo: {name}")

        if name not in self.metadata:
            raise FileNotFoundError(f"Photo '{name}' not found in storage")

        # Placeholder return
        return np.array([])

    def save_memory(
        self,
        video: np.ndarray,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Save an animated memory (video) with encryption.

        Args:
            video: Video as numpy array
            name: Name for the stored memory
            description: Optional description
            tags: Optional tags for organization
            metadata: Optional additional metadata (animation settings, etc.)

        Returns:
            Path to encrypted video file
        """
        # TODO: Implement video encryption and storage
        print(f"Saving encrypted memory: {name}")

        # Store metadata
        self.metadata[name] = {
            "type": "video",
            "description": description,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "animation_metadata": metadata or {}
        }
        self._save_metadata()

        # Placeholder return
        return self.storage_path / f"{name}.enc"

    def load_memory(
        self,
        name: str
    ) -> np.ndarray:
        """
        Load and decrypt an animated memory.

        Args:
            name: Name of the stored memory

        Returns:
            Video as numpy array

        Raises:
            FileNotFoundError: If memory doesn't exist
            ValueError: If decryption fails
        """
        # TODO: Implement video decryption and loading
        print(f"Loading encrypted memory: {name}")

        if name not in self.metadata:
            raise FileNotFoundError(f"Memory '{name}' not found in storage")

        # Placeholder return
        return np.array([])

    def export_memory(
        self,
        name: str,
        output_path: Union[str, Path],
        format: str = "mp4"
    ):
        """
        Export a memory to unencrypted video file.

        Use this when you want to share the memory with others.

        Args:
            name: Name of the stored memory
            output_path: Path for exported file
            format: Video format ("mp4", "mov", "avi")
        """
        # TODO: Implement export
        print(f"Exporting memory '{name}' to {output_path}")
        print("Warning: Exported file will NOT be encrypted")

    def list_memories(
        self,
        memory_type: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        List all stored memories.

        Args:
            memory_type: Filter by type ("photo" or "video")
            tags: Filter by tags

        Returns:
            List of memory metadata
        """
        memories = []

        for name, meta in self.metadata.items():
            # Filter by type
            if memory_type and meta.get("type") != memory_type:
                continue

            # Filter by tags
            if tags:
                if not any(tag in meta.get("tags", []) for tag in tags):
                    continue

            memories.append({
                "name": name,
                **meta
            })

        return memories

    def delete_memory(
        self,
        name: str,
        confirm: bool = False
    ):
        """
        Delete a stored memory.

        This is permanent. The memory will be gone forever.

        Args:
            name: Name of the memory to delete
            confirm: Must be True to actually delete

        Raises:
            ValueError: If confirm is not True
        """
        if not confirm:
            raise ValueError(
                "Deleting memories is permanent. "
                "Set confirm=True to proceed."
            )

        if name not in self.metadata:
            raise FileNotFoundError(f"Memory '{name}' not found")

        # TODO: Implement actual file deletion
        print(f"Deleting memory: {name}")
        print("This cannot be undone.")

        del self.metadata[name]
        self._save_metadata()

    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about stored memories.

        Returns:
            Dictionary with storage statistics
        """
        total_photos = sum(1 for m in self.metadata.values() if m.get("type") == "photo")
        total_videos = sum(1 for m in self.metadata.values() if m.get("type") == "video")

        return {
            "total_memories": len(self.metadata),
            "photos": total_photos,
            "videos": total_videos,
            "storage_path": str(self.storage_path),
            "encrypted": True,
            "encryption_type": "AES-256"
        }
