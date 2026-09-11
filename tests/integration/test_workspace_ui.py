"""Exercise the actual workspace UI without credentials or external services."""

from pathlib import Path

import pytest

testing = pytest.importorskip("streamlit.testing.v1")
APP = Path(__file__).resolve().parents[2] / "src/musicweb/web/app.py"


def workspace():
    return testing.AppTest.from_file(str(APP), default_timeout=45).run()


def click(app, label):
    next(button for button in app.button if button.label == label).click().run()
    assert not app.exception
    assert not app.error


def test_empty_workspace_exposes_all_tools():
    app = workspace()
    assert not app.exception
    assert not app.error
    assert [tab.label for tab in app.tabs] == [
        "Overview",
        "Compare",
        "Analyze",
        "Playlist audit",
        "YTM dedup",
        "Playlist cleanup",
        "Enrich",
        "Help",
    ]
    assert app.sidebar.file_uploader[0].accept_multiple_files
    assert any("Upload a library to begin." in item.value for item in app.markdown)


def test_uploaded_libraries_compare_analyze_and_export():
    app = workspace()
    uploader = app.sidebar.file_uploader[0]
    if not hasattr(uploader, "set_value"):
        pytest.skip("This Streamlit version does not support testing file uploads")

    header = "Track Name,Artist Name(s),Album Name,Duration (ms),ISRC\n"
    shared = "Shared Song,Example Artist,Record,180000,USAAA2600001\n"
    unique = "Only Here,Another Artist,Record,210000,USAAA2600002\n"
    uploader.set_value(
        [
            ("source.csv", (header + shared + unique).encode(), "text/csv"),
            ("target.csv", (header + shared).encode(), "text/csv"),
        ]
    ).run()
    click(app, "Load source.csv")
    click(app, "Load target.csv")
    assert len(app.session_state.libraries) == 2
    assert {m.label: m.value for m in app.metric}["Total tracks"] == "3"

    click(app, "Compare Libraries")
    metrics = {m.label: m.value for m in app.metric}
    assert metrics["Total matches"] == "1"
    assert metrics["Missing tracks"] == "1"
    assert metrics["Match rate"] == "50.0%"
    assert len(app.get("download_button")) == 2
    assert len(app.get("plotly_chart")) == 5

    click(app, "Analyze Libraries")
    assert len(app.session_state.analysis_results["universal_tracks"]) == 1
    # Subsequent widget reruns must keep the comparison and its exports available.
    assert len(app.session_state.comparison_results) == 1
    assert len(app.get("download_button")) >= 2
