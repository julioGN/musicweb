"""
External service integrations for MusicWeb.

This module provides integrations with external music services
including YouTube Music API, playlist management, and deduplication services.
"""

from .deduplication import DeduplicationService
from .playlist import PlaylistManager
from .youtube_music import YouTubeMusicAPI

__all__ = ["YouTubeMusicAPI", "PlaylistManager", "DeduplicationService"]
