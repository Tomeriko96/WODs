"""
Configuration settings for the WOD Browser application.
"""

import streamlit as st


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="WOD Browser",
        page_icon="🏋️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# Application constants
APP_TITLE = "🏋️ WOD Browser"
APP_DESCRIPTION = "Browse, search, filter, and discover workout ideas from the WODs repository"

# File settings
SUPPORTED_EXTENSIONS = [".md", ".txt"]
EXCLUDED_DIRECTORIES = ["resources"]

# UI settings
ITEMS_PER_PAGE = 10

DEFAULT_RSS_FEEDS = [
    "https://trainingthinktank.com/blog/feed/",
    "https://crossfitexplode.com/feed/",
    "https://invictusfitness.com/feed/",
    "https://krigertraining.com/feed/",
    "https://pushjerk.com/feed/",
    "https://www.crossfitcardiff.com/blog?format=rss",
    "https://crossfitvalor.com/wod?format=rss",
]

# GitHub settings
GITHUB_REPO = "Tomeriko96/WODs"