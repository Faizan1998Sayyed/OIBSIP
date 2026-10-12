"""
Main Launcher Entry Point for Random Password Generator
Supports Tkinter GUI mode (default) and CLI mode (--cli).
"""

import sys
import cli_app
import gui_app

def main():
    if "--cli" in sys.argv or "-c" in sys.argv:
        cli_app.run_cli()
    else:
        gui_app.main()

if __name__ == "__main__":
    main()
