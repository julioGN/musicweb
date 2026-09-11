"""Shared presentation for MusicWeb's ink-and-paper workspace."""

import base64
import math
from html import escape
from pathlib import Path

import streamlit as st


def apply_theme():
    """Load packaged styles without browser scripts or external assets."""
    css = (Path(__file__).parent / "styles" / "web.css").read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def web_image():
    """Draw fine radial threads and curved rings inspired by the logo."""

    def point(radius, angle):
        return 200 + radius * math.cos(angle), 200 + radius * math.sin(angle)

    angles = [i * math.pi / 4 for i in range(8)]
    paths = []
    for angle in angles:
        x, y = point(190, angle)
        paths.append(f'<path d="M200 200 L{x:.2f} {y:.2f}"/>')
    for radius in (30, 62, 98, 140, 180):
        for angle in angles:
            x1, y1 = point(radius, angle)
            x2, y2 = point(radius, angle + math.pi / 4)
            cx, cy = point(radius * 0.77, angle + math.pi / 8)
            paths.append(
                f'<path d="M{x1:.2f} {y1:.2f} Q{cx:.2f} {cy:.2f} {x2:.2f} {y2:.2f}"/>'
            )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">'
        '<g fill="none" stroke="#898980" stroke-width=".8">'
        + "".join(paths)
        + '</g><circle cx="200" cy="200" r="4" fill="#252620"/></svg>'
    )
    return base64.b64encode(svg.encode()).decode()


def render_empty_state(message):
    """Show the next action for a library-dependent tool."""
    st.markdown(
        f'<section class="mw-empty"><div class="mw-empty-copy">'
        f"<h2>{escape(message)}</h2>"
        f'</div><img class="mw-web" src="data:image/svg+xml;base64,{web_image()}" '
        'alt="" aria-hidden="true"/></section>',
        unsafe_allow_html=True,
    )


def render_chart(fig):
    """Use a restrained, legible palette for all interactive charts."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#f8f8f3",
        plot_bgcolor="#f8f8f3",
        font=dict(family="Arial, sans-serif", color="#252620"),
        colorway=["#252620", "#7a8174", "#b6bcac", "#777064", "#a3a59b"],
        margin=dict(l=24, r=24, t=56, b=40),
    )
    # Plotly Express binds colors to traces before layout defaults are applied.
    palette = ["#252620", "#7a8174", "#b6bcac", "#777064", "#a3a59b"]
    for i, trace in enumerate(fig.data):
        if trace.type == "pie":
            trace.marker.colors = palette
        elif trace.type in ("bar", "histogram"):
            trace.marker.color = palette[i % len(palette)]
    st.plotly_chart(fig, use_container_width=True, theme=None)
