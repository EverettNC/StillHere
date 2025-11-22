#!/usr/bin/env python3
"""
Funeral Avatar Pipeline - Automated Processing

Handles the chaos of family sending photos/videos at different times.
Processes everything automatically. Ready when you are.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess
import json

# Add stillhere to path
sys.path.insert(0, str(Path(__file__).parent))

def extract_audio_from_videos(video_dir: Path, output_dir: Path):
    """
    Extract audio from all videos in a folder.
    Handles any format - MP4, MOV, AVI, etc.
    """
    video_dir = Path(video_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("EXTRACTING AUDIO FROM VIDEOS")
    print("=" * 70)
    print()
    
    # Find all video files
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.m4v', '.flv']
    videos = []
    for ext in video_extensions:
        videos.extend(video_dir.glob(f'*{ext}'))
        videos.extend(video_dir.glob(f'*{ext.upper()}'))
    
    if not videos:
        print(f"No videos found in {video_dir}")
        return []
    
    print(f"Found {len(videos)} videos")
    print()
    
    audio_files = []
    
    for i, video in enumerate(videos, 1):
        print(f"[{i}/{len(videos)}] Processing: {video.name}")
        
        # Output audio file
        audio_file = output_dir / f"{video.stem}_audio.wav"
        
        try:
            # Extract audio with ffmpeg
            # -vn: no video
            # -acodec pcm_s16le: high quality PCM audio
            # -ar 44100: 44.1kHz sample rate
            cmd = [
                'ffmpeg', '-y', '-i', str(video),
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # PCM 16-bit
                '-ar', '44100',  # 44.1kHz
                '-ac', '1',  # Mono (easier for voice cloning)
                str(audio_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and audio_file.exists():
                duration = get_audio_duration(audio_file)
                print(f"  ✓ Extracted: {audio_file.name} ({duration:.1f}s)")
                audio_files.append(audio_file)
            else:
                print(f"  ✗ Failed to extract audio")
                
        except subprocess.TimeoutExpired:
            print(f"  ✗ Timeout processing video")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()
    
    print(f"Successfully extracted {len(audio_files)} audio files")
    print()
    
    return audio_files


def get_audio_duration(audio_file: Path) -> float:
    """Get duration of audio file in seconds."""
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_file)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return 0.0


def find_best_voice_sample(audio_files: list, target_duration: float = 15.0) -> Path:
    """
    Find the best audio sample for voice cloning.
    
    Criteria:
    - 5-30 seconds duration (ideal: 10-20s)
    - Clear audio (no music/background noise - manual check needed)
    - Natural speech
    """
    print("=" * 70)
    print("SELECTING BEST VOICE SAMPLE")
    print("=" * 70)
    print()
    
    candidates = []
    
    for audio_file in audio_files:
        duration = get_audio_duration(audio_file)
        
        # Score based on duration
        if 5 <= duration <= 30:
            # Prefer 10-20 second clips
            if 10 <= duration <= 20:
                score = 10
            elif 5 <= duration <= 10 or 20 <= duration <= 25:
                score = 7
            else:
                score = 5
            
            candidates.append({
                'file': audio_file,
                'duration': duration,
                'score': score
            })
    
    if not candidates:
        print("No suitable voice samples found (need 5-30 seconds)")
        return None
    
    # Sort by score
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print("Voice sample candidates:")
    for i, c in enumerate(candidates[:5], 1):  # Show top 5
        print(f"{i}. {c['file'].name} - {c['duration']:.1f}s (score: {c['score']})")
    
    print()
    best = candidates[0]['file']
    print(f"Selected: {best.name}")
    print()
    
    return best


def combine_audio_samples(audio_files: list, output_file: Path, max_duration: float = 30.0):
    """
    Combine multiple short audio clips into one sample.
    Useful if all clips are very short.
    """
    print("Combining audio samples...")
    
    # Create concat list for ffmpeg
    concat_file = output_file.parent / "concat_list.txt"
    with open(concat_file, 'w') as f:
        total_duration = 0
        for audio in audio_files:
            duration = get_audio_duration(audio)
            if total_duration + duration <= max_duration:
                f.write(f"file '{audio.absolute()}'\n")
                total_duration += duration
    
    # Concatenate with ffmpeg
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_file),
        '-c', 'copy',
        str(output_file)
    ]
    
    subprocess.run(cmd, capture_output=True)
    concat_file.unlink()
    
    if output_file.exists():
        print(f"✓ Combined sample created: {output_file.name}")
        return output_file
    
    return None


def process_photos(photo_dir: Path, output_dir: Path):
    """
    Find and process photos.
    Selects highest quality images.
    """
    photo_dir = Path(photo_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("PROCESSING PHOTOS")
    print("=" * 70)
    print()
    
    # Find all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.heif']
    photos = []
    for ext in image_extensions:
        photos.extend(photo_dir.glob(f'*{ext}'))
        photos.extend(photo_dir.glob(f'*{ext.upper()}'))
    
    if not photos:
        print(f"No photos found in {photo_dir}")
        return []
    
    print(f"Found {len(photos)} photos")
    print()
    
    # Sort by file size (higher quality = bigger file usually)
    photos.sort(key=lambda p: p.stat().st_size, reverse=True)
    
    print("Top photos by quality:")
    for i, photo in enumerate(photos[:10], 1):
        size_mb = photo.stat().st_size / (1024 * 1024)
        print(f"{i}. {photo.name} ({size_mb:.1f} MB)")
    
    print()
    
    # Copy top photos to output
    selected = photos[:5]  # Keep top 5
    for photo in selected:
        import shutil
        dest = output_dir / photo.name
        shutil.copy(photo, dest)
        print(f"✓ Copied: {photo.name}")
    
    print()
    return selected


def main():
    """
    Main pipeline - run this when videos/photos arrive.
    """
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "FUNERAL AVATAR PROCESSING PIPELINE" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Setup
    base_dir = Path(__file__).parent
    input_videos = base_dir / "funeral_materials" / "videos"
    input_photos = base_dir / "funeral_materials" / "photos"
    output_dir = base_dir / "funeral_materials" / "processed"
    
    input_videos.mkdir(parents=True, exist_ok=True)
    input_photos.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Input folders:")
    print(f"  Videos: {input_videos}")
    print(f"  Photos: {input_photos}")
    print(f"Output: {output_dir}")
    print()
    
    # Check if we have materials
    has_videos = any(input_videos.iterdir())
    has_photos = any(input_photos.iterdir())
    
    if not has_videos and not has_photos:
        print("⚠ No materials found yet.")
        print()
        print("Family should send files to:")
        print(f"  Videos → {input_videos}")
        print(f"  Photos → {input_photos}")
        print()
        print("Run this script again when files arrive.")
        return
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'audio_files': [],
        'best_voice_sample': None,
        'photos': []
    }
    
    # Process videos
    if has_videos:
        audio_dir = output_dir / "audio_extracted"
        audio_files = extract_audio_from_videos(input_videos, audio_dir)
        results['audio_files'] = [str(f) for f in audio_files]
        
        if audio_files:
            best_voice = find_best_voice_sample(audio_files)
            if best_voice:
                results['best_voice_sample'] = str(best_voice)
                
                # Copy to easy location
                final_voice = output_dir / "VOICE_SAMPLE_FOR_AVATAR.wav"
                import shutil
                shutil.copy(best_voice, final_voice)
                print(f"✓ Voice sample ready: {final_voice}")
                print()
    
    # Process photos
    if has_photos:
        photo_output = output_dir / "photos_selected"
        selected_photos = process_photos(input_photos, photo_output)
        results['photos'] = [str(p) for p in selected_photos]
        
        if selected_photos:
            best_photo = selected_photos[0]
            final_photo = output_dir / f"BEST_PHOTO_FOR_AVATAR{best_photo.suffix}"
            import shutil
            shutil.copy(best_photo, final_photo)
            print(f"✓ Best photo ready: {final_photo}")
            print()
    
    # Save results
    results_file = output_dir / "processing_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)
    print()
    print("Ready files:")
    if results['best_voice_sample']:
        print(f"  ✓ Voice: {output_dir}/VOICE_SAMPLE_FOR_AVATAR.wav")
    if results['photos']:
        print(f"  ✓ Photo: {output_dir}/BEST_PHOTO_FOR_AVATAR.*")
    print()
    
    if results['best_voice_sample'] and results['photos']:
        print("🎬 READY TO CREATE FUNERAL AVATAR")
        print()
        print("Next step:")
        print(f"  python create_funeral_avatar.py")
    else:
        if not results['best_voice_sample']:
            print("⚠ Need voice sample (from video with her talking)")
        if not results['photos']:
            print("⚠ Need photos")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcessing stopped.\n")
    except Exception as e:
        print(f"\nError: {e}\n")
        import traceback
        traceback.print_exc()
