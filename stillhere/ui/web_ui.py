"""
Web UI - Web interface for StillHere.

A gentle, respectful web interface for creating living memories.

Built with simplicity and compassion in mind.
"""

from typing import Optional
from pathlib import Path
import sys


class WebUI:
    """
    Web interface for StillHere.

    Provides a compassionate, easy-to-use web interface for:
    - Uploading photos
    - Creating animations
    - Restoring photos
    - Managing memories
    - Exporting and sharing

    Example:
        >>> ui = WebUI(port=5000)
        >>> ui.run()
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 5000,
        debug: bool = False
    ):
        """
        Initialize the web UI.

        Args:
            host: Host to bind to (default: localhost)
            port: Port to bind to (default: 5000)
            debug: Enable debug mode
        """
        self.host = host
        self.port = port
        self.debug = debug
        self.app = None

    def _create_app(self):
        """Create a minimal Flask app providing a Memorial creation form.

        The implementation is intentionally lightweight: if `flask` is not
        installed the method will raise ImportError with guidance. The route
        delegates to `scripts/create_memorial.py` to build the final MP4 so
        we avoid importing that script as a module.
        """
        try:
            from flask import Flask, request, send_file, render_template_string
        except Exception as e:  # pragma: no cover - runtime dependency
            raise ImportError(
                "Flask is required for the web UI. Install with: pip install flask"
            ) from e

        app = Flask(__name__)

        # Simple HTML form for memorial creation
        FORM_HTML = """
        <!doctype html>
        <html>
        <head><title>Create Memorial</title></head>
        <body>
          <h1>Create Memorial Slideshow</h1>
          <form method="post" action="/memorial" enctype="multipart/form-data">
            <label>Title: <input type="text" name="title" /></label><br/>
            <label>Music (optional): <input type="file" name="music" /></label><br/>
            <label>Image duration (s): <input type="number" name="image_duration" value="6" /></label><br/>
            <label>Crossfade (s): <input type="number" name="crossfade" value="1.0" step="0.1" /></label><br/>
            <label>FPS: <input type="number" name="fps" value="30" /></label><br/>
            <label>Width: <input type="number" name="width" value="1920" /></label>
            <label>Height: <input type="number" name="height" value="1080" /></label><br/>
            <label>Photos / Clips (select multiple): <input type="file" name="inputs" multiple /></label><br/>
            <button type="submit">Create Memorial</button>
          </form>
        </body>
        </html>
        """

        @app.route('/', methods=['GET'])
        def index():
            return render_template_string(FORM_HTML)

        @app.route('/memorial', methods=['POST'])
        def memorial():
            import tempfile
            import shutil
            import subprocess
            out_dir = Path('test_output')
            out_dir.mkdir(parents=True, exist_ok=True)

            tmp = Path(tempfile.mkdtemp(prefix='stillhere_memorial_'))
            inputs = []

            # Save uploaded files
            files = request.files.getlist('inputs')
            for up in files:
                if up and up.filename:
                    dest = tmp / up.filename
                    up.save(dest)
                    inputs.append(str(dest))

            music_file = request.files.get('music')
            music_path = None
            if music_file and music_file.filename:
                music_path = str(tmp / music_file.filename)
                music_file.save(music_path)

            captions_file = request.files.get('captions')
            captions_path = None
            if captions_file and captions_file.filename:
                captions_path = str(tmp / captions_file.filename)
                captions_file.save(captions_path)

            title = request.form.get('title') or None
            # Assemble per-file captions from form fields named caption_<filename>
            captions_tmp = tmp / 'captions.csv'
            wrote = False
            with captions_tmp.open('w', encoding='utf-8') as ch:
                for key in request.form:
                    if key.startswith('caption_'):
                        fname = key[len('caption_'):]
                        cap = request.form.get(key)
                        if cap and fname:
                            safe = cap.replace('"', '""')
                            ch.write(f'"{fname}","{safe}"\n')
                            wrote = True
            if wrote:
                captions_path = str(captions_tmp)

            image_duration = float(request.form.get('image_duration') or 6.0)
            crossfade = float(request.form.get('crossfade') or 1.0)
            fps = int(request.form.get('fps') or 30)
            width = int(request.form.get('width') or 1920)
            height = int(request.form.get('height') or 1080)

            output_path = out_dir / f"memorial_{tmp.name}.mp4"

            cmd = [sys.executable, str(Path('scripts') / 'create_memorial.py')]
            cmd += inputs
            cmd += ['-o', str(output_path)]
            if title:
                cmd += ['--title', title]
            if music_path:
                cmd += ['--music', music_path]
            cmd += ['--image-duration', str(image_duration), '--crossfade', str(crossfade), '--fps', str(fps), '--width', str(width), '--height', str(height)]

            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                shutil.rmtree(tmp, ignore_errors=True)
                return f"Error creating memorial: {e}", 500

            # Clean up uploads but keep output
            shutil.rmtree(tmp, ignore_errors=True)

            # Return the resulting file for download
            if output_path.exists():
                return send_file(str(output_path), as_attachment=True)
            return "Failed to create memorial", 500

        return app

    def run(self):
        """Run the web interface."""
        try:
            if self.app is None:
                self.app = self._create_app()
        except ImportError as e:
            print(str(e))
            return

        print(f"\nStarting StillHere Web UI...")
        print(f"URL: http://{self.host}:{self.port}")
        print("\nPress Ctrl+C to stop")
        print("\n" + "=" * 60)
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def stop(self):
        """Stop the web interface."""
        print("Stopping StillHere Web UI...")


def main():
    """Main entry point for web UI."""
    import argparse

    parser = argparse.ArgumentParser(description="StillHere Web Interface")
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    ui = WebUI(host=args.host, port=args.port, debug=args.debug)
    ui.run()


if __name__ == '__main__':
    main()
