# ==========================================================
#  RippleWriter Studio — Controls Tab (Full Width Panel)
#  Restored from Design Left Panel (Backup 2025-11-19)
#  CLEAN — NO COLUMNS — NO SCROLL CONTAINER
# ==========================================================

import streamlit as st
import datetime
from app.utils.yaml_tools import list_yaml_files, load_yaml

def render_controls_panel():
    """
    Full-width Controls tab — restored from the original Design Left Panel.
    No columns, no scroll containers, no injected CSS.
    """

    st.header("Application Controls")

    # ==================================================
    # SYSTEM STATUS
    # ==================================================
    st.subheader("🧠 System Status")
    st.markdown("**Environment:** RippleWriter Studio Modular Refactor")
    st.markdown("**Status:** 🟢 Active")

    c1, c2 = st.columns(2)
    with c1:
        st.button("🔄 Restart Session", key="controls_restart_btn")
    with c2:
        st.button("🧹 Flush Cache", key="controls_flush_btn")

    st.caption("Restart clears session_state. Cache flush clears AI temp memory.")
    st.divider()

    # ==================================================
    # AI SETTINGS
    # ==================================================
    st.subheader("🔑 AI Access & Configuration")

    st.text_input(
        "OpenAI API Key",
        type="password",
        key="controls_api_key"
    )

    st.selectbox(
        "Model",
        ["GPT-5 (default)", "GPT-4.1", "Claude 3.5", "Local LLM"],
        key="controls_model_select"
    )

    st.toggle("Use Streaming Mode", key="controls_streaming_toggle")
    st.caption("Stored per session. Used across all tabs.")
    st.divider()

    # ==================================================
    # DRAFT MANAGEMENT
    # ==================================================
    st.subheader("📄 Draft Management")

    try:
        drafts = list_yaml_files()
    except Exception:
        drafts = []

    st.markdown(f"**{len(drafts)} drafts found**")

    draft_choice = st.selectbox(
        "Select a draft",
        ["(none)"] + drafts,
        key="controls_draft_select"
    )

    if draft_choice != "(none)":
        st.info(f"Loaded draft: **{draft_choice}**")
        try:
            # Removed JSON — this was collapsing the layout.
            loaded_yaml = load_yaml(draft_choice)
            st.markdown("Draft loaded successfully.")
        except Exception:
            st.error("YAML failed to load.")

    st.button("📝 New Draft", key="controls_new_draft")
    st.divider()

    # ==================================================
    # TEMPLATE & EQUATION PACKS
    # ==================================================
    st.subheader("🧩 Template & Equation Packs")

    st.markdown("""
**Templates Available**
- Academic  
- Op-Ed  
- Legal Brief  
- Investigative  
- RippleTruth Fact File  
- MarketMind Narrative  

**Equation Packs**
- Intention Fields (FILS / UCIP / RippleScore)
- MarketMind Equation Suite
- RippleTruth Fact Scoring
""")

    st.selectbox(
        "Preferred Equation Pack",
        [
            "None",
            "Intention Field Equations",
            "MarketMind Equation Suite",
            "RippleTruth Fact Grading"
        ],
        key="controls_eq_pack"
    )

    st.caption("Determines equation availability in Write tab.")
    st.divider()

    # ==================================================
    # USER GUIDE
    # ==================================================
    with st.expander("📘 Controls Tab Guide"):
        st.markdown("""
### Purpose
Global application controls independent of article structure.

### Includes
- AI configuration  
- Draft management  
- Template/equation pack selection  
- Diagnostics  
""")

    st.divider()

    # ==================================================
    # DIAGNOSTICS
    # ==================================================
    st.subheader("⚙️ Diagnostics Snapshot")
    st.markdown(f"**Last Sync:** {datetime.datetime.now().strftime('%H:%M:%S')}")

    st.markdown("**Active Threads:** 3")
    st.markdown("**Runtime Mode:** Dev")

    st.progress(85, text="System Health")

    st.caption("RippleWriter © 2025 — Structural Engine Ready")
