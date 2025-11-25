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
    <p>Write your own. Retort the rest.</p>
</div>
""",
    unsafe_allow_html=True
)

# Break the header container so layout resets cleanly
st.write("")


# ============================================================
# ROUTER: Monitor → Design auto-switch (safe 2-step method)
# ============================================================
if st.session_state.get("go_to_design"):
    st.session_state["go_to_design"] = False      # reset the flag
    st.session_state["active_tab"] = "Design"     # switch tab
    st.rerun()

# ------------------------------------------------------------
# Tabs (NOW 6 TABS, Monitor moved to the end)
# ------------------------------------------------------------
tab_design, tab_write, tab_analyze, tab_export, tab_controls, tab_ripplechat, tab_monitor = st.tabs(
    [
        "Design",
        "Write",
        "Analyze",
        "Export",
        "Controls",
        "RippleChat AI",
        "Monitor"
    ]
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

/* ---------------------------------------------------------- */
/*   RIPPLEWRITER — MONITOR TAB (Guaranteed, DOM-Verified)     */
/* ---------------------------------------------------------- */

/* Make the 7th tab (Monitor) larger, bold, GOLD */
button[data-testid="stTab"]:nth-of-type(7) p {
    font-size: 18px !important;
    font-weight: 800 !important;
    color: #d4cf8c !important;   /* same gold tone as your message box */
    letter-spacing: 0.4px !important;
}

/* Make Monitor’s icon gold (◎) */
button[data-testid="stTab"]:nth-of-type(7) p::before {
    content: "◎ ";
    font-size: 18px !important;
    color: #d4cf8c !important;
    margin-right: 4px;
}

/* Make RippleChat AI robot icon NOT gold (reset to normal) */
button[data-testid="stTab"]:nth-of-type(6) span[aria-label="robot_face"] {
    color: inherit !important;
}

/* Add stronger underline when Monitor is active */
button[data-testid="stTab"][aria-selected="true"]:nth-of-type(7) 
    + div[data-baseweb="tab-highlight"] {
    height: 4px !important;
    background: linear-gradient(90deg, #ff4444, #cc2222) !important;
    border-radius: 3px;
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

# ============================================================
# DESIGN TAB — COLUMN-FREE PANEL
# ============================================================
with tab_design:

    # Remove Streamlit padding (gives true full-width design workspace)
    st.markdown(
        """
        <style>
            section.main > div.block-container {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Import new design panel safely
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

# ================================================
#  RippleChat AI — Clean Chat Interface (Option B)
# ================================================
with tab_ripplechat:

    st.markdown("## 🤖 RippleChat AI")
    st.markdown("Ask anything. Inject story context. Draft ideas. Rewrite. Analyze. Retort.")

    # ------------------------------
    # Session state for chat messages
    # ------------------------------
    if "ripplechat_messages" not in st.session_state:
        st.session_state.ripplechat_messages = []

    # -----------------------------------------
    # Chat message rendering (ChatGPT-style UI)
    # -----------------------------------------
    for msg in st.session_state.ripplechat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # -----------------------------------------
    # Inject context from Design tab
    # -----------------------------------------
    st.markdown("---")
    if st.button("📌 Inject Current Article Context"):
        from design_panel import get_current_design_context

        context_text = get_current_design_context()

        if context_text:
            st.session_state.ripplechat_messages.append(
                {"role": "user", "content": f"(context injected)\n\n{context_text}"}
            )
            with st.chat_message("user"):
                st.write(context_text)
        else:
            st.warning("No article context found in Design tab.")

    st.markdown("---")

    # ------------------------------
    # User input box (ChatGPT style)
    # ------------------------------
    user_input = st.chat_input("Type your message...")

    if user_input:
        # show user message immediately
        st.session_state.ripplechat_messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.write(user_input)

        # ---------------------------------
        # Simple placeholder LLM call
        # (you can replace with GPT-4/4o API)
        # ---------------------------------
        def ripple_llm(prompt: str) -> str:
            return f"RippleChat AI received: **{prompt}**\n\n(LLM integration goes here.)"

        response = ripple_llm(user_input)

        # show assistant message
        st.session_state.ripplechat_messages.append(
            {"role": "assistant", "content": response}
        )
        with st.chat_message("assistant"):
            st.write(response)


# ============================================================
# FLOATING RIPPLEWRITER ASSISTANT — GLOBAL OVERLAY
# Safe to place above the footer (does not affect layout)
# ============================================================

# Initialize toggle
if "rw_assistant_open" not in st.session_state:
    st.session_state.rw_assistant_open = False

# Floating button CSS
st.markdown(
    """
    <style>
        /* Floating Button */
        #rw-help-button {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 999999;
            background: #20252b;
            border: 1px solid #444;
            padding: 12px 16px;
            border-radius: 12px;
            color: #ff4b5c;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            transition: 0.25s ease-in-out;
        }

        #rw-help-button:hover {
            background: #2f353d;
            transform: scale(1.05);
        }

        /* Floating panel container */
        .rw-assistant-panel {
            position: fixed;
            bottom: 80px;
            right: 30px;
            width: 380px;
            max-height: 500px;
            overflow-y: auto;
            background: #1b1f24;
            border: 1px solid #444;
            border-radius: 12px;
            padding: 20px;
            z-index: 999998;
            color: #ddd;
            box-shadow: 0 6px 16px rgba(0,0,0,0.45);
        }

        .rw-assistant-panel h3 {
            margin-top: 0;
            color: #ff4b5c;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
#  Footer
# ----------------------------------------------------------
st.markdown("---")
st.caption("RippleWriter © Kevin Day — New Modular Panel Build (2025)")




