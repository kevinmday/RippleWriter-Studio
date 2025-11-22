# ==========================================================
# RippleWriter Studio — WRITE TAB ROUTER (2025 Modular Build)
# Unified Write Tab — full-width working area
# ==========================================================

import streamlit as st

# Correct import
from refactor_regions.studio_panels.write.write_panel import render_write_panel


def render_write_tab():
    """Load the new unified Write tab panel."""
    try:
        render_write_panel()
    except Exception as e:
        st.error(f"Write tab failed: {e}")
