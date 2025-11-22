# ==========================================================
#  RippleWriter Studio — Design Tab (Left Panel)
#  FIXED HEIGHT • CONTINUOUS • INDEPENDENT SCROLL
# ==========================================================

import streamlit as st
import datetime
from app.utils.yaml_tools import list_yaml_files, load_yaml

def render_design_left(colA):

    with colA:

        # --------------------------------------------------
        # FIX: Make left column a full-height scroll panel
        # --------------------------------------------------
        st.markdown("""
<style>
    .design-left-pane {
        height: 88vh;              /* Full column height */
        overflow-y: auto;          /* Independent scroll */
        padding-right: 12px;       /* Prevent cutoff */
    }
</style>
<div class="design-left-pane">
""", unsafe_allow_html=True)

        # ==================================================
        # SYSTEM STATUS
        # ==================================================
        st.header("Design Controls")

        st.subheader("🧠 System Status")
        st.markdown("**Environment:** RippleWriter Studio Modular Refactor")
        st.markdown("**Status:** 🟢 Active")

        # ==================================================
        # AI SETTINGS
        # ==================================================
        st.subheader("🔑 AI Access & Configuration")

        st.text_input(
            "OpenAI API Key",
            type="password",
            key="design_api_key"
        )

        st.selectbox(
            "Model",
            ["GPT-5 (default)", "GPT-4.1", "Claude 3.5", "Local LLM"],
            key="design_model_select"
        )

        st.toggle("Use Streaming Mode", key="design_streaming_toggle")
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
            key="design_left_draft_select"
        )

        # ❗ REMOVED RAW YAML PREVIEW — ROOT CAUSE OF LAYOUT BLOAT
        if draft_choice != "(none)":
            st.info(f"Loaded draft: **{draft_choice}**")

        st.button("📝 New Draft", key="design_left_new_draft")
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
            key="design_left_eq_pack"
        )

        st.caption("Determines equation availability in Write tab.")
        st.divider()

        # ==================================================
        # USER GUIDE
        # ==================================================
        with st.expander("📘 Design Tab Guide"):
            st.markdown("""
### Purpose
Structure your article before writing begins.

### Workflow
1. Choose a template  
2. Set metadata  
3. Edit YAML structure  
4. Save draft  
5. Move to Write tab to begin writing  
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

        # --------------------------------------------------
        # CLOSE SCROLL CONTAINER
        # --------------------------------------------------
        st.markdown("</div>", unsafe_allow_html=True)
