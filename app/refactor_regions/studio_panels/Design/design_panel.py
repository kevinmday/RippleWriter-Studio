# ==========================================================
#  RippleWriter Studio — DESIGN PANEL (2025 Modular Build)
#  Receives payload from Monitor and auto-populates metadata
#  YAML Integration: /yaml/system + /yaml/templates
#  CLEAN METADATA + COMPOSE AREA ONLY (Write tab does the rest)
# ==========================================================

import streamlit as st
import os

from app.utils.yaml_tools import (
    list_yaml_files,
    load_yaml,
    save_yaml,
)

# ----------------------------------------------------------
# YAML ROOTS
# ----------------------------------------------------------
SYSTEM_PATH = "app/yaml/system"
TEMPLATES_PATH = "app/yaml/templates"


# ----------------------------------------------------------
# SAFELY LOAD AVAILABLE YAML FILES
# ----------------------------------------------------------
def get_yaml_options():
    system_files = list_yaml_files(SYSTEM_PATH)
    template_files = list_yaml_files(TEMPLATES_PATH)
    return system_files + template_files


# ----------------------------------------------------------
# DESIGN PANEL — MAIN FUNCTION
# ----------------------------------------------------------
def render_design_panel():

    st.markdown("## ✏️ RippleWriter — Design Workspace")
    st.caption("Articles auto-load here when you click headlines from the Monitor tab.")

    # ------------------------------------------------------
    # 1. Detect incoming payload from Monitor
    # ------------------------------------------------------
    payload = st.session_state.get("design_payload")

    if payload:
        st.info("🛰️ Auto-imported from Monitor feed.")
    else:
        st.warning("Waiting for a headline click from Monitor…")
        payload = {}

    # ------------------------------------------------------
    # AUTO-PREFILL SESSION STATE (the missing critical piece)
    # ------------------------------------------------------
    if payload and not st.session_state.get("design_prefilled", False):

        st.session_state["design_title"] = payload.get("title", "")
        st.session_state["design_summary"] = payload.get("summary", "")
        st.session_state["design_source"] = payload.get("source", "")
        st.session_state["design_timestamp"] = payload.get("timestamp", "")
        st.session_state["design_author"] = payload.get("author", "")
        st.session_state["design_url"] = payload.get("url", "")

        # initial body seed
        st.session_state["design_body"] = (
            payload.get("summary", "") + "\n\n(Continue writing here…)"
        )

        # prevents re-seeding on rerun
        st.session_state["design_prefilled"] = True

    # ------------------------------------------------------
    # Extract values from session_state (guaranteed accurate)
    # ------------------------------------------------------
    title     = st.session_state.get("design_title", "")
    summary   = st.session_state.get("design_summary", "")
    source    = st.session_state.get("design_source", "")
    timestamp = st.session_state.get("design_timestamp", "")
    author    = st.session_state.get("design_author", "")
    url       = st.session_state.get("design_url", "")

    # ------------------------------------------------------
    # 2. Metadata Input Region
    # ------------------------------------------------------
    with st.expander("🧩 Article Metadata", expanded=True):

        st.text_input("Headline", key="design_title")
        st.text_area("Summary", key="design_summary", height=100)

        colA, colB, colC = st.columns(3)

        with colA:
            st.text_input("Source", key="design_source")

        with colB:
            st.text_input("Timestamp", key="design_timestamp")

        with colC:
            st.text_input("Author", key="design_author")

        st.text_input("Original Article URL", key="design_url")

    # ------------------------------------------------------
    # 3. BODY COMPOSITION AREA
    # ------------------------------------------------------
    st.markdown("### 📝 Draft Article Text")
    st.caption("Light editing space. For full writing tools, go to the Write tab.")

    st.text_area(
        label="Compose Here",
        key="design_body",
        height=300,
    )

    # ------------------------------------------------------
    # 4. YAML Saving + Retrieval
    # ------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📦 Save / Load Article as YAML")

    yaml_files = get_yaml_options()
    selected_yaml = st.selectbox("Load existing YAML", ["(None)"] + yaml_files)

    col1, col2 = st.columns(2)

    # ------------------------------------------------------
    # LOAD YAML
    # ------------------------------------------------------
    with col1:
        if selected_yaml != "(None)":
            if st.button("Load YAML"):
                try:
                    data = load_yaml(selected_yaml)

                    # Unified field names
                    st.session_state["design_title"] = data.get("title", "")
                    st.session_state["design_summary"] = data.get("summary", "")
                    st.session_state["design_body"] = data.get("body", "")
                    st.session_state["design_source"] = data.get("source", "")
                    st.session_state["design_timestamp"] = data.get("timestamp", "")
                    st.session_state["design_author"] = data.get("author", "")
                    st.session_state["design_url"] = data.get("url", "")

                    st.success(f"Loaded: {selected_yaml}")

                except Exception as e:
                    st.error(f"Failed to load YAML: {e}")

    # ------------------------------------------------------
    # SAVE YAML
    # ------------------------------------------------------
    with col2:

        filename = st.text_input(
            "Filename (e.g., article1.yaml)",
            key="design_save_name",
            value="article_draft.yaml"
        )

        if st.button("Save YAML"):
            if filename:
                data = {
                    "title": st.session_state.get("design_title", ""),
                    "summary": st.session_state.get("design_summary", ""),
                    "source": st.session_state.get("design_source", ""),
                    "timestamp": st.session_state.get("design_timestamp", ""),
                    "author": st.session_state.get("design_author", ""),
                    "url": st.session_state.get("design_url", ""),
                    "body": st.session_state.get("design_body", ""),
                }

                try:
                    save_yaml(filename, data)
                    st.success(f"Saved: {filename}")
                except Exception as e:
                    st.error(f"Save failed: {e}")

    st.markdown("---")
    st.success("Design tab ready. Click headlines in Monitor to send more stories over.")
