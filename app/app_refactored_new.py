# ==========================================================
#  RippleWriter Studio – NEW Modular Router (safe parallel)
#  Version: Panel Architecture (Design / Write / Analyze / Export)
# ==========================================================
import streamlit as st
from pathlib import Path
import sys

# ----------------------------------------------------------
#  Path Setup (kept identical for safety)
# ----------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
    print(f"✅ RippleWriter root added to sys.path: {ROOT_DIR}")


# ----------------------------------------------------------
#  Handle floating button JS callback (Write fullscreen exit)
# ----------------------------------------------------------
if st.session_state.get("write_fullscreen") and st.session_state.get("_component_value") == "exit":
    st.session_state.write_fullscreen = False
    st.session_state["_component_value"] = None
    st.rerun()


# ----------------------------------------------------------
#  Streamlit Config
# ----------------------------------------------------------
st.set_page_config(
    page_title="RippleWriter Studio",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------
#  Initialize Canonical Session State Keys
# ----------------------------------------------------------
REQUIRED_KEYS = [
    "draft_text",
    "draft_yaml",

    "analysis_raw_output",
    "insights_text",
    "rippletruth_report",
    "intent_metrics",

    "export_title",
    "export_subtitle",
    "export_html",
    "export_markdown",

    "analysis_data",
    "analysis_mode",
    "analysis_trigger",

    "export_format",

    "include_final",
    "include_insights",
    "include_rippletruth",
    "include_intention_metrics",
    ]

for key in REQUIRED_KEYS:
    if key not in st.session_state:
        st.session_state[key] = ""

# ---------------------------------------------------------------
# Branding + Header (Padding Fix + Safe Visibility Margin)
# ---------------------------------------------------------------
st.markdown(
    """
<style>
/* Remove Streamlit's default excessive top padding */
section.main > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* SAFE top space so the header is ALWAYS visible */
.header-wrap {
    margin-top: 2.2rem;      /* <-- adjust this if needed */
    margin-bottom: 1.6rem;
}

/* Typography tuning */
.header-wrap h1 {
    margin-bottom: 0px;
    font-size: 2.6rem;
    font-weight: 600;
}

.header-wrap p {
    margin-top: -6px;
    font-size: 1.1rem;
    color: #ccc;
}
</style>

<div class="header-wrap">
    <h1>RippleWriter Studio</h1>
    <p>New modular build — Design • Write • Analyze • Export</p>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# ROUTER: Monitor → Design auto-switch (safe 2-step method)
# ============================================================
if st.session_state.get("go_to_design"):
    st.session_state["go_to_design"] = False      # reset the flag
    st.session_state["active_tab"] = "Design"     # switch tab
    st.rerun()

# ----------------------------------------------------------
# Tabs (NOW 6 TABS)
# ----------------------------------------------------------
tab_design, tab_write, tab_analyze, tab_export, tab_controls, tab_monitor = st.tabs(
    ["Design", "Write", "Analyze", "Export", "Controls", "Monitor"]
)

# ----------------------------------------------------------
#  Global Column Styling
# ----------------------------------------------------------
st.markdown(
    """
<style>
[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}
[data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    min-height: 100vh !important;
    justify-content: flex-start !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
#  Safe Import Helper
# ----------------------------------------------------------
def safe_import(module_path, function_name):
    try:
        module = __import__(module_path, fromlist=[function_name])
        return getattr(module, function_name)
    except Exception as e:
        st.error(f"⚠️ Import error in {module_path}.{function_name}: {e}")
        return None

# ==========================================================
#  DESIGN TAB — COLUMN-FREE PANEL
# ==========================================================
with tab_design:

    # Remove Streamlit padding
    st.markdown("""
        <style>
            section.main > div.block-container {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Import new design panel
    design_panel = safe_import(
        "app.refactor_regions.studio_panels.design.design_panel",
        "render_design_panel"
    )

    # Render single-panel design UI
    if design_panel:
        design_panel()

# ----------------------------------------------------------
# Write Tab (FULL WIDTH – UNIFIED WRITE PANEL)
# ----------------------------------------------------------
with tab_write:

    # Remove Streamlit padding
    st.markdown("""
        <style>
            section.main > div.block-container {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## Write")

    # Import unified write panel
    write_panel = safe_import(
        "app.refactor_regions.studio_panels.write.write_panel",
        "render_write_panel"
    )

    # Render if loaded
    if write_panel:
        write_panel()
    else:
        st.error("Write panel failed to load.")

# ----------------------------------------------------------
# Analyze Tab
# ----------------------------------------------------------
with tab_analyze:

    # Initialize session state placeholder for analysis results
    if "analysis_data" not in st.session_state:
        st.session_state.analysis_data = None

    # Import modular panels
    left_panel = safe_import(
        "app.refactor_regions.studio_panels.analyze.left_panel",
        "render_left_panel"
    )
    center_panel = safe_import(
        "app.refactor_regions.studio_panels.analyze.center_panel",
        "render_center_panel"
    )
    right_panel = safe_import(
        "app.refactor_regions.studio_panels.analyze.right_panel",
        "render_right_panel"
    )

    # Layout: three columns
    colA, colB, colC = st.columns([1.1, 2.0, 1.0])

    # Render left controls
    if left_panel:
        left_panel(colA)

    # Render main results
    if center_panel:
        center_panel(colB)

    # Render insights
    if right_panel:
        right_panel(colC)

with tab_export:

    colA, colB, colC = st.columns([1.1, 2.0, 1.0])

    left_panel = safe_import(
        "app.refactor_regions.studio_panels.export.left_panel",
        "render_left_panel"
    )
    center_panel = safe_import(
        "app.refactor_regions.studio_panels.export.center_panel",
        "render_center_panel"
    )
    right_panel = safe_import(
        "app.refactor_regions.studio_panels.export.right_panel",
        "render_right_panel"
    )

    if left_panel: left_panel(colA)
    if center_panel: center_panel(colB)
    if right_panel: right_panel(colC)

# ----------------------------------------------------------
# Controls Tab (FULL WIDTH – NO COLUMNS)
# ----------------------------------------------------------
with tab_controls:

    # Remove padding
    st.markdown("""
        <style>
            section.main > div.block-container {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## Controls")

    controls_panel = safe_import(
        "app.refactor_regions.studio_panels.controls.controls_panel",
        "render_controls_panel"
    )

    if controls_panel:
        controls_panel()

# ----------------------------------------------------------
#  Monitor Tab
# ----------------------------------------------------------
with tab_monitor:
    try:
        monitor_region = safe_import(
            "app.monitor.monitor_region",
            "render_monitor_region"
        )

        if monitor_region:
            monitor_region()
        else:
            st.error("⚠️ Monitor panel failed to load (import returned None).")

    except Exception as e:
        st.error(f"🔥 Monitor Panel Error: {e}")

# ----------------------------------------------------------
#  Footer
# ----------------------------------------------------------
st.markdown("---")
st.caption("RippleWriter © Kevin Day — New Modular Panel Build (2025)")




