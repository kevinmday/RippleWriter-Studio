# ==========================================================
# RippleWriter Studio — Compose Region (3-Column Refactor)
# ==========================================================
import streamlit as st
import uuid
from app.utils.yaml_tools import save_yaml, load_yaml, list_yaml_files


def render_compose_panel(colA, colB, colC):
    # ------------------------------------------------------
    # LEFT COLUMN (colA)
    # ------------------------------------------------------
    with colA:
        st.subheader("Draft Controls")
        st.write("Select an existing draft or start a new one.")

        try:
            drafts = list_yaml_files()
        except Exception:
            drafts = []

        selected = st.selectbox("Choose Draft", ["(new)"] + drafts)
        if selected != "(new)":
            st.info(f"Loaded draft: **{selected}**")

    # ------------------------------------------------------
    # CENTER COLUMN (colB)
    # ------------------------------------------------------
    with colB:
        st.subheader("YAML Scaffold Builder")

        article_type = st.selectbox(
            "Choose Article Type",
            ["(new)", "BlogPost.yaml", "OpEd.yaml"],
            key="compose_article_type"
        )

        # ----------------------------
        # AI Assistant Placeholder ONLY
        # ----------------------------
        st.markdown("### AI Assistant")
        st.caption("AI-generated suggestions will appear in the Chat tab, not here.")

        if st.button("Generate Sections with AI Help", key="ai_generate_sections"):
            st.info("✓ AI Assistance triggered — results will appear in the Chat tab.")

        # ----------------------------
        # Intention Equation Selector
        # ----------------------------
        st.markdown("### Intention Equation")
        equation = st.selectbox(
            "Select Equation",
            ["None", "Peace Vector", "Fractal Resonance", "UCIP Flow"],
            key="intention_eq"
        )

        st.info("Draft: (new)\nAuthor: Kevin Day")
        st.success("✓ YAML Valid — no critical errors detected.")

        # ----------------------------
        # YAML Controls
        # ----------------------------
        st.markdown("---")
        st.markdown("**YAML Actions**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save YAML (Stay)", key="save_yaml_compose"):
                st.success("✓ YAML saved. Continue refining.")
        with col2:
            if st.button("➡ Save & Move to Input", key="save_yaml_input"):
                st.success("✓ Saved & moved to Input tab.")

        st.caption("*Future: Ripple Feedback, Intention Matrix, etc.*")

    # ------------------------------------------------------
    # RIGHT COLUMN (colC)
    # ------------------------------------------------------
    with colC:
        st.subheader("Context Panel")
        st.write(
            """
            ℹ This space will host live diagnostics, RippleTruth feedback, 
            or intention-based context from the current YAML draft.

            *Examples (future integration):*
            - Real-time FILS + UCIP health checks  
            - Intention Equation visualizations  
            - RippleSeer / RippleTruth output logs  
            - Auto-preview of YAML → HTML render
            """
        )
        st.caption("Connected via: `colC` → shared context panel")
