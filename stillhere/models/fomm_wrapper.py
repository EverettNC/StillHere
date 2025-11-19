"""
FOMM Wrapper - First Order Motion Model integration for StillHere.

This module wraps the First Order Motion Model for photo animation.
It provides both real FOMM integration and a fallback demo mode.

For real animation, download models first:
    python download_models.py
"""

from typing import Optional, Union, List
from pathlib import Path
import numpy as np
import torch
from PIL import Image


class FOM

MModel:
    """
    First Order Motion Model wrapper.

    Handles loading, initialization, and inference of FOMM.
    """

    def __init__(
        self,
        checkpoint_path: Optional[Union[str, Path]] = None,
        config_path: Optional[Union[str, Path]] = None,
        device: str = "cuda",
        use_demo_mode: bool = False
    ):
        """
        Initialize FOMM.

        Args:
            checkpoint_path: Path to FOMM checkpoint file
            config_path: Path to FOMM config file
            device: Device to use ("cuda" or "cpu")
            use_demo_mode: Use demo mode if models not available
        """
        self.device = device if torch.cuda.is_available() else "cpu"
        self.checkpoint_path = checkpoint_path
        self.config_path = config_path
        self.use_demo_mode = use_demo_mode
        self.model = None
        self.kp_detector = None
        self.generator = None
        self._initialized = False

    def _load_real_model(self):
        """Load the actual FOMM model."""
        try:
            # Try to import FOMM modules
            # This requires the FOMM repository to be installed
            import sys
            fomm_path = Path(__file__).parent / "fomm"
            if fomm_path.exists():
                sys.path.insert(0, str(fomm_path))

            from modules.generator import OcclusionAwareGenerator
            from modules.keypoint_detector import KPDetector
            import yaml

            # Load config
            with open(self.config_path) as f:
                config = yaml.safe_load(f)

            # Load checkpoint
            checkpoint = torch.load(self.checkpoint_path, map_location=self.device)

            # Initialize generator
            self.generator = OcclusionAwareGenerator(
                **config['model_params']['generator_params'],
                **config['model_params']['common_params']
            )
            self.generator.load_state_dict(checkpoint['generator'])
            self.generator.to(self.device)
            self.generator.eval()

            # Initialize keypoint detector
            self.kp_detector = KPDetector(
                **config['model_params']['kp_detector_params'],
                **config['model_params']['common_params']
            )
            self.kp_detector.load_state_dict(checkpoint['kp_detector'])
            self.kp_detector.to(self.device)
            self.kp_detector.eval()

            print("✓ FOMM models loaded successfully")
            return True

        except Exception as e:
            print(f"⚠️  Could not load FOMM models: {e}")
            print("   Falling back to demo mode")
            return False

    def _create_demo_animation(
        self,
        source_image: np.ndarray,
        num_frames: int,
        style: str
    ) -> List[np.ndarray]:
        """
        Create a simple demo animation without FOMM.

        This creates a gentle "breathing" effect using basic transformations.

        Args:
            source_image: Source image
            num_frames: Number of frames to generate
            style: Animation style

        Returns:
            List of animated frames
        """
        frames = []
        h, w = source_image.shape[:2]

        for i in range(num_frames):
            # Create gentle breathing effect
            t = i / num_frames
            scale = 1.0 + 0.02 * np.sin(2 * np.pi * t)  # 2% scale variation

            # Calculate new dimensions
            new_h = int(h * scale)
            new_w = int(w * scale)

            # Resize image
            img = Image.fromarray(source_image)
            img_scaled = img.resize((new_w, new_h), Image.LANCZOS)

            # Crop/pad to original size
            frame = np.array(img_scaled)
            if scale > 1.0:
                # Crop center
                y_offset = (new_h - h) // 2
                x_offset = (new_w - w) // 2
                frame = frame[y_offset:y_offset+h, x_offset:x_offset+w]
            else:
                # Pad
                pad_h = (h - new_h) // 2
                pad_w = (w - new_w) // 2
                frame = np.pad(
                    frame,
                    ((pad_h, h - new_h - pad_h), (pad_w, w - new_w - pad_w), (0, 0)),
                    mode='edge'
                )

            frames.append(frame)

        return frames

    def animate(
        self,
        source_image: np.ndarray,
        driving_video: Optional[List[np.ndarray]] = None,
        num_frames: int = 150,
        style: str = "gentle"
    ) -> List[np.ndarray]:
        """
        Animate a source image.

        Args:
            source_image: Source image to animate
            driving_video: Optional driving video frames
            num_frames: Number of frames to generate (if no driving video)
            style: Animation style

        Returns:
            List of animated frames
        """
        # Check if real model is available
        if not self._initialized:
            if self.checkpoint_path and Path(self.checkpoint_path).exists():
                success = self._load_real_model()
                self._initialized = True
                if not success:
                    self.use_demo_mode = True
            else:
                print("⚠️  FOMM models not found. Using demo mode.")
                print("   Download models with: python download_models.py")
                self.use_demo_mode = True
                self._initialized = True

        # Use real model if available
        if not self.use_demo_mode and self.generator is not None:
            return self._animate_with_fomm(source_image, driving_video, num_frames)

        # Otherwise use demo mode
        return self._create_demo_animation(source_image, num_frames, style)

    def _animate_with_fomm(
        self,
        source_image: np.ndarray,
        driving_video: Optional[List[np.ndarray]],
        num_frames: int
    ) -> List[np.ndarray]:
        """
        Animate using real FOMM model.

        Args:
            source_image: Source image
            driving_video: Driving video frames
            num_frames: Number of frames

        Returns:
            Animated frames
        """
        # Preprocess source image
        source = torch.tensor(source_image[np.newaxis].astype(np.float32) / 255).permute(0, 3, 1, 2)
        source = source.to(self.device)

        # Get source keypoints
        with torch.no_grad():
            kp_source = self.kp_detector(source)

        # If no driving video, generate motion
        if driving_video is None:
            # Generate default motion (simple head movement)
            frames = []
            for i in range(num_frames):
                # Use source as driving (results in minimal motion)
                kp_driving = kp_source

                # Generate frame
                out = self.generator(source, kp_source=kp_source, kp_driving=kp_driving)
                frame = np.transpose(out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0]
                frame = (frame * 255).astype(np.uint8)
                frames.append(frame)
        else:
            # Use driving video
            frames = []
            for driving_frame in driving_video:
                driving = torch.tensor(driving_frame[np.newaxis].astype(np.float32) / 255).permute(0, 3, 1, 2)
                driving = driving.to(self.device)

                with torch.no_grad():
                    kp_driving = self.kp_detector(driving)
                    out = self.generator(source, kp_source=kp_source, kp_driving=kp_driving)

                frame = np.transpose(out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0]
                frame = (frame * 255).astype(np.uint8)
                frames.append(frame)

        return frames


def get_default_checkpoint_path() -> Optional[Path]:
    """
    Get the default FOMM checkpoint path.

    Returns:
        Path to checkpoint if it exists, None otherwise
    """
    checkpoint_dir = Path(__file__).parent / "fomm"
    checkpoint_file = checkpoint_dir / "vox-cpk.pth.tar"

    if checkpoint_file.exists():
        return checkpoint_file

    return None


def get_default_config_path() -> Optional[Path]:
    """
    Get the default FOMM config path.

    Returns:
        Path to config if it exists, None otherwise
    """
    config_dir = Path(__file__).parent / "fomm"
    config_file = config_dir / "vox-256.yaml"

    if config_file.exists():
        return config_file

    return None
