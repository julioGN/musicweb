"""
Core business logic for MusicWeb.

This module contains the fundamental data models and algorithms
for music library management and comparison.
"""

from .comparison import ComparisonResult, LibraryComparator
from .enrichment import EnrichmentManager
from .matching import TrackMatcher
from .models import Library, Track, TrackNormalizer

__all__ = [
    "Track",
    "Library",
    "TrackNormalizer",
    "LibraryComparator",
    "ComparisonResult",
    "TrackMatcher",
    "EnrichmentManager",
]
