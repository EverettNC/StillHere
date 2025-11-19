"""
CLI - Command Line Interface for StillHere.

A simple, respectful command-line interface for those who prefer it.

Because sometimes simplicity is best when dealing with grief.
"""

import argparse
from pathlib import Path
from typing import Optional
import sys


class CLI:
    """
    Command-line interface for StillHere.

    Example usage:
        $ python -m stillhere.ui.cli animate photo.jpg --style gentle_smile
        $ python -m stillhere.ui.cli restore photo.jpg --output restored.jpg
        $ python -m stillhere.ui.cli list
    """

    def __init__(self):
        """Initialize the CLI."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="StillHere - Bringing cherished memories to life",
            epilog="Built with love for those who deserve to be remembered."
        )

        subparsers = parser.add_subparsers(dest='command', help='Commands')

        # Animate command
        animate_parser = subparsers.add_parser(
            'animate',
            help='Animate a photo'
        )
        animate_parser.add_argument('photo', help='Path to photo')
        animate_parser.add_argument(
            '--style',
            default='gentle_smile',
            choices=['gentle_smile', 'breathing', 'head_turn', 'speaking', 'portrait', 'custom'],
            help='Animation style'
        )
        animate_parser.add_argument('--duration', type=float, default=5.0, help='Duration in seconds')
        animate_parser.add_argument('--output', '-o', help='Output video path')
        animate_parser.add_argument('--quality', default='high', choices=['low', 'medium', 'high'])
        animate_parser.add_argument('--passphrase', help='Encryption passphrase for storage')

        # Restore command
        restore_parser = subparsers.add_parser(
            'restore',
            help='Restore and enhance a photo'
        )
        restore_parser.add_argument('photo', help='Path to photo')
        restore_parser.add_argument('--output', '-o', required=True, help='Output photo path')
        restore_parser.add_argument('--upscale', type=int, default=1, choices=[1, 2, 4], help='Upscale factor')
        restore_parser.add_argument('--colorize', action='store_true', help='Colorize black & white photos')
        restore_parser.add_argument('--quality', default='high', choices=['low', 'medium', 'high'])

        # List command
        list_parser = subparsers.add_parser(
            'list',
            help='List stored memories'
        )
        list_parser.add_argument('--passphrase', required=True, help='Encryption passphrase')
        list_parser.add_argument('--type', choices=['photo', 'video'], help='Filter by type')

        # Export command
        export_parser = subparsers.add_parser(
            'export',
            help='Export a stored memory'
        )
        export_parser.add_argument('name', help='Name of the memory')
        export_parser.add_argument('output', help='Output file path')
        export_parser.add_argument('--passphrase', required=True, help='Encryption passphrase')

        # Info command
        info_parser = subparsers.add_parser(
            'info',
            help='Show information about StillHere'
        )

        return parser

    def run(self, args: Optional[list] = None):
        """
        Run the CLI.

        Args:
            args: Command-line arguments (default: sys.argv[1:])
        """
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return

        # Route to appropriate handler
        handler = getattr(self, f'_handle_{parsed_args.command}', None)
        if handler:
            handler(parsed_args)
        else:
            print(f"Unknown command: {parsed_args.command}")
            self.parser.print_help()

    def _handle_animate(self, args):
        """Handle the animate command."""
        print(f"\nAnimating: {args.photo}")
        print(f"Style: {args.style}")
        print(f"Duration: {args.duration}s")
        print(f"Quality: {args.quality}")

        # TODO: Implement actual animation
        from stillhere import Animator
        animator = Animator()

        # This will be replaced with real implementation
        print("\nNote: Animation functionality will be implemented in Phase 1")
        print("This is the project foundation - models will be added next.")

    def _handle_restore(self, args):
        """Handle the restore command."""
        print(f"\nRestoring: {args.photo}")
        print(f"Output: {args.output}")
        print(f"Upscale: {args.upscale}x")
        print(f"Colorize: {args.colorize}")
        print(f"Quality: {args.quality}")

        # TODO: Implement actual restoration
        from stillhere import Restorer
        restorer = Restorer()

        print("\nNote: Restoration functionality will be implemented in Phase 2")
        print("This is the project foundation - models will be added next.")

    def _handle_list(self, args):
        """Handle the list command."""
        print("\nStored Memories:")
        print("-" * 50)

        # TODO: Implement actual listing
        from stillhere import MemoryKeeper
        keeper = MemoryKeeper(args.passphrase)

        memories = keeper.list_memories(memory_type=args.type)

        if not memories:
            print("No memories stored yet.")
        else:
            for memory in memories:
                print(f"\n{memory['name']} ({memory['type']})")
                if memory.get('description'):
                    print(f"  {memory['description']}")
                if memory.get('tags'):
                    print(f"  Tags: {', '.join(memory['tags'])}")

    def _handle_export(self, args):
        """Handle the export command."""
        print(f"\nExporting: {args.name}")
        print(f"To: {args.output}")

        # TODO: Implement actual export
        from stillhere import MemoryKeeper
        keeper = MemoryKeeper(args.passphrase)

        keeper.export_memory(args.name, args.output)
        print("\nWarning: Exported file is NOT encrypted")

    def _handle_info(self, args):
        """Handle the info command."""
        print("\n" + "=" * 60)
        print("StillHere - Bringing cherished memories to life")
        print("=" * 60)
        print("\nNot a replacement for who we've lost.")
        print("A way to honor them. To remember them. To hold onto their presence.")
        print("\nBuilt with love for those who deserve to be remembered.")
        print("\n" + "-" * 60)
        print("\nCommands:")
        print("  animate  - Animate a photo into gentle video")
        print("  restore  - Enhance and restore old photos")
        print("  list     - List stored memories")
        print("  export   - Export a memory to share")
        print("  info     - Show this information")
        print("\nFor help on a command:")
        print("  python -m stillhere.ui.cli <command> --help")
        print("\n" + "=" * 60)
        print('\n"Grief is love with nowhere to go.')
        print('Let\'s give it somewhere to be."')
        print("=" * 60 + "\n")


def main():
    """Main entry point for CLI."""
    cli = CLI()
    cli.run()


if __name__ == '__main__':
    main()
