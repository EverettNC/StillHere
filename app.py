#!/usr/bin/env python3
"""
StillHere - Main Application Entry Point

Bringing cherished memories to life through AI-powered photo animation.

Not a replacement for who we've lost.
A way to honor them. To remember them. To hold onto their presence.

Built with love for those who deserve to be remembered.

Usage:
    # Run web interface
    python app.py

    # Run CLI
    python app.py --cli

    # Show help
    python app.py --help
"""

import argparse
import sys
from pathlib import Path


def print_banner():
    """Print the StillHere banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║                          StillHere                               ║
    ║                                                                  ║
    ║        Bringing cherished memories to life through AI            ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝

    Not a replacement for who we've lost.
    A way to honor them. To remember them. To hold onto their presence.

    Built with love for those who deserve to be remembered.
    """
    print(banner)


def print_quote():
    """Print the closing quote."""
    print('\n    "Grief is love with nowhere to go.')
    print('     Let\'s give it somewhere to be."\n')


def run_web_ui(host: str = "127.0.0.1", port: int = 5000, debug: bool = False):
    """
    Run the web interface.

    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    from stillhere.ui.web_ui import WebUI

    print_banner()
    print(f"    Starting web interface at http://{host}:{port}")
    print("    Press Ctrl+C to stop\n")

    ui = WebUI(host=host, port=port, debug=debug)
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n\n    Goodbye. Be gentle with yourself.")
        print_quote()
        sys.exit(0)


def run_cli(args: list):
    """
    Run the command-line interface.

    Args:
        args: Command-line arguments
    """
    from stillhere.ui.cli import CLI

    cli = CLI()
    cli.run(args)


def main():
    """Main entry point for StillHere."""
    parser = argparse.ArgumentParser(
        description="StillHere - Bringing cherished memories to life",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run web interface
  python app.py

  # Run web interface on specific port
  python app.py --port 8080

  # Run CLI to animate a photo
  python app.py --cli animate photo.jpg --style gentle_smile

  # Run CLI to restore a photo
  python app.py --cli restore old_photo.jpg --output restored.jpg

  # Get CLI help
  python app.py --cli --help

Built with tears and love. For those who deserve to be remembered.
        """
    )

    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI mode instead of web UI'
    )

    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (web UI only, default: 127.0.0.1)'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind to (web UI only, default: 5000)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )

    # Parse known args to allow passing additional args to CLI
    args, unknown = parser.parse_known_args()

    if args.version:
        from stillhere import __version__, __author__
        print(f"StillHere v{__version__}")
        print(f"By {__author__}")
        print_quote()
        return

    if args.cli:
        # Run in CLI mode
        run_cli(unknown)
    else:
        # Run in web UI mode
        if unknown:
            print(f"Warning: Unknown arguments will be ignored in web UI mode: {unknown}\n")
        run_web_ui(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye. Be gentle with yourself.")
        print_quote()
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        if '--debug' in sys.argv:
            raise
        sys.exit(1)
