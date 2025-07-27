#!/usr/bin/env python3
"""
WOD Browser - A modular Streamlit application for browsing workout files.

Main entry point for the application.
"""

from src.config import configure_page
from src.browser import WODBrowser


def main():
    """Main entry point for the WOD Browser application."""
    # Configure Streamlit page settings
    configure_page()
    
    # Initialize and run the WOD Browser
    app = WODBrowser()
    app.run()


if __name__ == "__main__":
    main()