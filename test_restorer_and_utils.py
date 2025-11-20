import os
import tempfile
import numpy as np
from pathlib import Path
from stillhere.core.restorer import Restorer
from stillhere.models.fomm_wrapper import FOMMModel
from stillhere.core.utils import ImageUtils


def make_test_image(w=64, h=64, color=(128, 128, 128)):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    arr[..., 0] = color[0]
    arr[..., 1] = color[1]
    arr[..., 2] = color[2]
    # Add a simple synthetic 'scratch' (line)
    arr[h//2, 5:-5] = [255, 255, 255]
    return arr


def test_restorer_enhance_returns_array():
    restorer = Restorer()
    img = make_test_image()
    out = restorer.enhance(img, fix_scratches=True, fix_blur=True, colorize=False, upscale=1, denoise=True, quality='high')
    assert isinstance(out, np.ndarray)
    assert out.ndim == 3 and out.shape[2] == 3


def test_restorer_upscale_keeps_aspect():
    restorer = Restorer()
    img = make_test_image(40, 20)
    out = restorer.upscale_image(img, scale=2, quality='medium')
    assert isinstance(out, np.ndarray)
    assert out.shape[1] == 40*2 and out.shape[0] == 20*2


def test_restorer_colorize_basic():
    restorer = Restorer()
    # Create a low-contrast grayscale-like image
    gray = np.full((32, 32, 3), 120, dtype=np.uint8)
    out = restorer.colorize_photo(gray, intensity=0.8)
    assert isinstance(out, np.ndarray)
    assert out.shape == gray.shape


def test_fomm_demo_animation_length_and_shape():
    # Ensure demo animation returns correct number of frames and shape
    fomm = FOMMModel(use_demo_mode=True)
    img = make_test_image(64, 64)
    frames = fomm.animate(img, driving_video=None, num_frames=10, style='breathing')
    assert isinstance(frames, list)
    assert len(frames) == 10
    for fr in frames:
        assert isinstance(fr, np.ndarray)
        assert fr.shape[0] == 64 and fr.shape[1] == 64 and fr.shape[2] == 3


def test_imageutils_load_and_save(tmp_path):
    img = make_test_image(32, 48)
    p = tmp_path / 'test_img.png'
    ImageUtils.save_image(img, p)
    loaded = ImageUtils.load_image(p, as_rgb=True)
    assert isinstance(loaded, np.ndarray)
    assert loaded.shape[0] == 48 and loaded.shape[1] == 32


if __name__ == '__main__':
    import pytest
    pytest.main([-q, __file__])
