"""
Utility functions for MusicWeb.

This module contains common utilities for file handling,
validation, logging, and other cross-cutting concerns.
"""

from .file_utils import detect_encoding, get_file_info, validate_file_size
from .logging import get_logger, setup_logging
from .validation import validate_library_data, validate_track_data

__all__ = [
    "detect_encoding",
    "validate_file_size",
    "get_file_info",
    "validate_track_data",
    "validate_library_data",
    "setup_logging",
    "get_logger",
]
