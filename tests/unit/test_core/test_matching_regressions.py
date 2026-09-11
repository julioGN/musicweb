"""Behavioral regressions for library matching and playlist scoring."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from musicweb.core.comparison import LibraryComparator
from musicweb.core.models import Library, Track, TrackMatcher, TrackNormalizer
import musicweb.core.models as models


def load_helper(name, relative_path):
    # Isolate these pure helpers from package initializers: integrations has a
    # pre-existing missing export, while web.__init__ starts the Streamlit app.
    path = Path(models.__file__).parent.parent / relative_path
    spec = importlib.util.spec_from_file_location("musicweb.core." + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


playlist = load_helper("_playlist_regression", "integrations/playlist.py")
audit = load_helper("_audit_regression", "web/playlist_audit.py")
PlaylistManager = playlist.PlaylistManager
PlaylistItem = audit.PlaylistItem
audit_playlist = audit.audit_playlist


def library(name, tracks):
    result = Library(name)
    result.add_tracks(tracks)
    return result


def compare(source, targets, comparator=None):
    return (comparator or LibraryComparator()).compare_libraries(
        library("source", [source]), library("target", targets)
    )


@pytest.mark.parametrize(
    "artist,variant",
    [
        ("AC/DC", "AC DC"),
        ("Beyoncé", "Beyonce"),
        ("Earth, Wind & Fire", "Earth Wind and Fire"),
        ("Radiohead", "Radiohed"),
    ],
)
def test_artist_variants_match(artist, variant):
    source = Track("Signal", artist, duration=180)
    target = Track("Signal", variant, duration=180)
    result = compare(source, [target])
    assert result.matches[0].target_track is target


def test_artist_credit_cleanup_preserves_names_and_collaborators():
    assert TrackNormalizer.normalize_artist("Daft Punk") == "daft punk"
    assert TrackNormalizer.normalize_artist("Daft Punk feat. Pharrell") == "daft punk"
    assert TrackNormalizer.extract_artist_tokens("Nova; Echo & Vega") == {
        "nova",
        "echo",
        "vega",
    }
    assert not compare(Track("Signal", "Daft Punk"), [Track("Signal", "Da")]).matches


@pytest.mark.parametrize("artist", ["Metallica", "Jason"])
def test_same_title_and_duration_do_not_rescue_wrong_artist(artist):
    assert not compare(
        Track("Signal", "Mason", duration=180),
        [Track("Signal", artist, duration=180)],
    ).matches


@pytest.mark.parametrize("position", [0, 50, 101])
def test_short_names_match_at_any_candidate_position(position):
    source = Track("Go", "AA", duration=180)
    target = Track("Go", "AA & BB", duration=180)
    candidates = [Track(f"Unrelated {i}", "ZZ") for i in range(101)]
    candidates.insert(position, target)
    result = compare(source, candidates)
    assert result.matches[0].target_track is target


def test_word_overlap_does_not_hide_better_spelling_match():
    source = Track("Northern Starlight", "Radiohead", duration=180)
    distractor = Track("Northern Horizon", "Someone Else", duration=180)
    target = Track("Northrn Starlite", "Radiohed", duration=180)
    for candidates in ([distractor, target], [target, distractor]):
        result = compare(source, candidates)
        assert result.matches[0].target_track is target


def test_reused_comparator_never_returns_previous_library_track():
    comparator = LibraryComparator()
    old = Track("Go", "AA", duration=180)
    compare(
        Track("Other Songs", "Nova"), [old, Track("Other Song", "Nova")], comparator
    )
    target = Track("Go", "AA & BB", duration=180)
    result = compare(Track("Go", "AA", duration=180), [target], comparator)
    assert result.matches[0].target_track is target


def test_mutated_candidate_list_invalidates_index():
    matcher = TrackMatcher()
    source = Track("Go", "AA", duration=180)
    candidates = [Track("Go", "AA", duration=180)]
    assert matcher.find_best_match(source, candidates)
    replacement = Track("Go", "AA & BB", duration=180)
    candidates[:] = [replacement]
    assert matcher.find_best_match(source, candidates)[0] is replacement
    replacement.is_music = False
    assert matcher.find_best_match(source, candidates) is None


@pytest.mark.parametrize(
    "title",
    [
        "Rain",
        "Talk",
        "Sleep",
        "Nature",
        "Signal (Explicit)",
        "Signal (Live from Wembley)",
    ],
)
def test_music_titles_are_eligible(title):
    source, target = Track(title, "Nova"), Track(title, "Nova")
    result = compare(source, [target])
    assert result.music_source_tracks == result.music_target_tracks == 1
    assert result.matches[0].target_track is target


@pytest.mark.parametrize(
    "title",
    [
        "Music Podcast Episode 12",
        "Guitar Tutorial",
        "Guided Meditation",
    ],
)
def test_explicit_non_music_indicators_still_filter(title):
    assert not Track(title, "Host").is_music


@pytest.mark.parametrize(
    "title,variant",
    [
        ("Signal [Live]", "Signal (Live)"),
        ("Signal [Radio Edit]", "Signal (Radio Edit)"),
        ("Signal", "Signal - 2011 Remaster"),
        ("Signal", "Signal (Official Audio)"),
        ("Signal", "Signal [feat. Echo]"),
    ],
)
def test_equivalent_annotations_match(title, variant):
    assert compare(Track(title, "Nova"), [Track(variant, "Nova")]).matches


@pytest.mark.parametrize(
    "variant",
    [
        "Signal [Live]",
        "Signal (Acoustic)",
        "Signal - Remix",
        "Signal [Radio Edit]",
        "Signal (Instrumental)",
    ],
)
def test_different_recordings_do_not_match_studio(variant):
    for source_title, target_title in [("Signal", variant), (variant, "Signal")]:
        assert not compare(
            Track(source_title, "Nova", duration=180),
            [Track(target_title, "Nova", duration=180)],
        ).matches


def test_distinct_song_parts_do_not_match():
    assert not compare(
        Track("Signal (Part One)", "Nova", duration=180),
        [Track("Signal (Part Two)", "Nova", duration=180)],
    ).matches


def test_isrc_precedes_version_and_metadata_matches():
    source = Track("Signal", "Nova", isrc=" USABC1234567 ")
    metadata_match = Track("Signal", "Nova")
    identity_match = Track("Alternate [Live]", "Echo", isrc="usabc1234567")
    targets = [metadata_match, identity_match]
    result = compare(source, targets)
    assert result.matches[0].target_track is identity_match
    assert result.matches[0].match_type == "isrc"
    assert TrackMatcher().find_best_match(source, targets)[0] is identity_match


def test_blank_isrc_does_not_match_unrelated_tracks():
    source = Track("Signal", "Nova", isrc=" ")
    target = Track("Elsewhere", "Someone Else", isrc=" ")
    assert not compare(source, [target]).matches
    assert TrackMatcher().find_best_match(source, [target]) is None


def test_featured_artist_named_live_is_not_a_recording_marker():
    assert compare(
        Track("Signal (feat. Live)", "Nova"), [Track("Signal", "Nova")]
    ).matches


def test_incompatible_exact_candidate_does_not_hide_compatible_recording():
    source = Track("Signal [Live]", "Nova", duration=180)
    ambiguous = Track("Signal Live", "Nova", duration=180)
    target = Track("Signal (Live at Wembley)", "Nova", duration=180)
    result = compare(source, [ambiguous, target])
    assert result.matches[0].target_track is target


def test_playlist_audit_allows_artist_spelling_variants():
    result = audit_playlist(
        [PlaylistItem("Signal", "Radiohead", duration=180)],
        library("target", [Track("Signal", "Radiohed", duration=180)]),
    )
    assert len(result["present"]) == 1


def test_playlist_search_uses_corrected_scoring_without_api_calls():
    manager = PlaylistManager()
    manager.ytmusic = Mock()
    manager.ytmusic.search.return_value = [
        {
            "title": "Signal [Live]",
            "artists": [{"name": "AC DC"}],
            "duration": "3:00",
            "resultType": "song",
            "videoId": "live",
        },
        {
            "title": "Signal",
            "artists": [{"name": "AC DC"}],
            "duration": "3:00",
            "resultType": "song",
            "videoId": "studio",
        },
    ]
    result = manager.find_best_match(Track("Signal", "AC/DC", duration=180))
    assert result["youtube_track"]["videoId"] == "studio"
