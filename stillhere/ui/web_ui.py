"""
Web UI - Web interface for StillHere.

A gentle, respectful web interface for creating living memories.

Built with simplicity and compassion in mind.
"""

from typing import Optional
from pathlib import Path


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
        """Create the Flask/FastAPI app."""
        # TODO: Implement web framework
        # Will use Flask or FastAPI for simplicity
        print("Creating web application...")
        print("This will be implemented in Phase 2")

    def run(self):
        """Run the web interface."""
        print(f"\nStarting StillHere Web UI...")
        print(f"URL: http://{self.host}:{self.port}")
        print("\nPress Ctrl+C to stop")
        print("\n" + "=" * 60)
        print("Note: Web UI will be implemented in Phase 2")
        print("This is the project foundation - UI will be added next.")
        print("=" * 60 + "\n")

        # TODO: Implement actual web server
        # self.app.run(host=self.host, port=self.port, debug=self.debug)

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
