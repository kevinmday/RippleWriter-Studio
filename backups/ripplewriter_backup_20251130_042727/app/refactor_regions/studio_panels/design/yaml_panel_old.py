# ==========================================================
#  RippleWriter Studio — Design Tab (YAML Panel)
#  Full-width block (outside columns)
# ==========================================================

import streamlit as st
import datetime
from app.utils.yaml_tools import load_yaml, save_yaml, list_yaml_files


def render_design_yaml():
    st.header("Design: YAML Draft Builder")

    # ------------------------------------------------------
    # DRAFT SELECTION
    # ------------------------------------------------------
    st.subheader("Select or Create Draft")

    drafts = []
    try:
        drafts = list_yaml_files()
    except:
        pass

    draft_choice = st.selectbox(
        "Choose Draft",
        ["(new)"] + drafts,
        key="design_yaml_select"
    )

    current_yaml = {}

    if draft_choice != "(new)":
        try:
            current_yaml = load_yaml(draft_choice)
        except:
            st.error("YAML failed to load.")

    st.markdown("---")

    # ------------------------------------------------------
    # TEMPLATE TYPE
    # ------------------------------------------------------
    st.subheader("Template Type")

    template = st.selectbox(
        "Choose Template",
        ["None", "Academic", "Op-Ed", "Investigative", "Legal Brief", "RippleTruth File", "MarketMind Narrative"],
        key="design_yaml_template"
    )

    st.button("Generate Template Structure", key="design_generate_template_btn")

    st.markdown("---")

    # ------------------------------------------------------
    # METADATA SECTION
    # ------------------------------------------------------
    st.subheader("Metadata")

    title = st.text_input("Title", value=current_yaml.get("title", ""))
    author = st.text_input("Author", value=current_yaml.get("author", "Kevin Day"))
    date = st.text_input("Date", value=current_yaml.get("date", datetime.date.today().isoformat()))

    st.markdown("---")

    # ------------------------------------------------------
    # YAML EDITOR
    # ------------------------------------------------------
    st.subheader("YAML Editor (Full Structure)")

    yaml_text = st.text_area(
        "Edit YAML",
        value=str(current_yaml).replace("{", "").replace("}", "").replace("'", ""),
        height=300,
        key="design_yaml_editor_text"
    )

    st.markdown("---")

    # ------------------------------------------------------
    # SAVE DRAFT
    # ------------------------------------------------------
    st.subheader("Save Draft")

    filename = st.text_input("Save as filename (e.g., article.yaml)", key="design_yaml_save_name")

    if st.button("💾 Save YAML Draft", key="design_yaml_save_btn"):
        if not filename.strip():
            st.error("Filename cannot be empty.")
        else:
            try:
                save_yaml(filename, yaml_text)
                st.success(f"Saved: {filename}")
            except Exception as e:
                st.error(f"Save failed: {e}")

    st.caption("Design Center — Structured Draft Builder")
