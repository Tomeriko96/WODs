"""
Browser module for the main WOD browsing functionality.
"""

from .wod_browser import WODBrowser
from .filters import WorkoutFilter

__all__ = ['WODBrowser', 'WorkoutFilter']