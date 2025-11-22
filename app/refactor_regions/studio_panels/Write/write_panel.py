# ==========================================================
# RippleWriter Studio — Unified WRITE TAB (2025 Modular Build)
# • Uses yaml/templates + yaml/models
# • Full-width writing flow
# ==========================================================

import streamlit as st
from app.utils.yaml_tools import (
    list_templates,
    load_template,
    load_model
)
import yaml
from datetime import datetime


# ----------------------------------------------------------
# RENDER WRITE PANEL
# ----------------------------------------------------------
def render_write_panel():

    st.title("✍️ Write Panel")
    st.caption("Full-width working area — draft → preview → export")
    st.markdown("---")

    # ======================================================
    # LOAD YAML RESOURCES
    # ======================================================

    # Load available article templates
    template_files = list_templates()
    template_names = [p.name for p in template_files]

    # Equation & intention models
    equations = load_model("equations.yaml")
    intention = load_model("intention.yaml")

    # ======================================================
    # TEMPLATE SELECTION
    # ======================================================
    st.subheader("Document Template")

    selected_file = st.selectbox(
        "Choose a Template",
        ["(none selected)"] + template_names
    )

    selected_template = (
        load_template(selected_file)
        if selected_file in template_names
        else None
    )

    st.markdown("---")

    # ======================================================
    # METADATA INPUT
    # ======================================================
    st.subheader("Metadata")

    title = st.text_input("Title")
    subtitle = st.text_input("Subtitle")
    author = st.text_input("Author", value="Kevin Day")

    st.markdown("---")

    # ======================================================
    # TEMPLATE YAML DISPLAY
    # ======================================================
    with st.expander("📄 View YAML Template Block", expanded=False):
        if selected_template:
            st.json(selected_template)
        else:
            st.info("No template selected — nothing to display.")

    st.markdown("---")

    # ======================================================
    # DRAFT EDITOR
    # ======================================================
    st.subheader("Draft Editor")

    draft_text = st.text_area(
        "Write or Edit Draft",
        height=350,
        placeholder="Start writing your article here..."
    )

    st.markdown("---")

    # ======================================================
    # GENERATE FROM TEMPLATE
    # ======================================================
    st.subheader("AI Writer")

    if st.button("✨ Generate Draft from Template"):
        if not selected_template:
            st.error("No document template selected.")
        else:
            sections = selected_template.get("sections", [])

            # Build a structured outline
            template_output = "\n\n".join([f"## {sec}" for sec in sections])

            combined = (
                f"# {title}\n\n"
                f"### {subtitle}\n\n"
                f"{template_output}"
            )

            st.success("Draft generated!")
            st.text_area("Generated Draft", combined, height=350)

    st.markdown("---")

    # ================================
    # LIVE HTML PREVIEW
    # ================================
    st.subheader("Live Preview (HTML)")

    # SAFE: no backslashes inside f-string expressions
    safe_text = draft_text.replace("\n", "<br>")

    html_preview = (
        f"<h1>{title}</h1>"
        f"<h3>{subtitle}</h3>"
        f"<p>{safe_text}</p>"
    )

    st.markdown(html_preview, unsafe_allow_html=True)

    st.markdown("---")

    st.caption("Write tab — unified full-width architecture (2025)")
