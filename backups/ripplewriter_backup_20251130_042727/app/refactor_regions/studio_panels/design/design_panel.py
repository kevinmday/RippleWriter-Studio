# ==========================================================
#  RippleWriter Studio — DESIGN PANEL (2025 Safe-Mode Build)
#  • Receives payload from Monitor
#  • Auto-populates metadata safely
#  • Saves YAML
#  • NEW: “Send to Write Tab” → stages metadata for Write panel
# ==========================================================

import streamlit as st
import yaml

from app.utils.yaml_tools import (
    list_yaml_files,
    load_yaml,
    save_yaml,
)

from app.refactor_regions.studio_state.write_state import WriteState


# ----------------------------------------------------------
# YAML ROOT PATHS
# ----------------------------------------------------------
SYSTEM_PATH = "app/yaml/system"
TEMPLATES_PATH = "app/yaml/templates"


# ----------------------------------------------------------
# SAFELY LOAD YAML OPTIONS
# ----------------------------------------------------------
def get_yaml_options():
    system_files = list_yaml_files(SYSTEM_PATH)
    template_files = list_yaml_files(TEMPLATES_PATH)
    return system_files + template_files


# ----------------------------------------------------------
# DESIGN PANEL — MAIN ENTRY
# ----------------------------------------------------------
def render_design_panel():

    st.markdown("## ✏️ RippleWriter — Design Workspace")
    st.caption("Articles auto-load here when you click headlines from the Monitor tab.")

    # ------------------------------------------------------
    # 1. Retrieve payload from Monitor (if any)
    # ------------------------------------------------------
    payload = st.session_state.get("design_payload")

    if payload:
        st.info("🛰️ Auto-imported from Monitor feed.")
    else:
        st.warning("Waiting for a headline click from Monitor…")
        payload = {}

    # ------------------------------------------------------
    # 2. Auto-prefill metadata (only once per payload)
    # ------------------------------------------------------
    if payload and not st.session_state.get("design_prefilled", False):

        st.session_state["design_title"] = payload.get("title", "")
        st.session_state["design_summary"] = payload.get("summary", "")
        st.session_state["design_source"] = payload.get("source", "")
        st.session_state["design_timestamp"] = payload.get("timestamp", "")
        st.session_state["design_author"] = payload.get("author", "")
        st.session_state["design_url"] = payload.get("url", "")

        st.session_state["design_body"] = (
            payload.get("summary", "") + "\n\n(Continue writing here…)"
        )

        st.session_state["design_prefilled"] = True

    # ------------------------------------------------------
    # 3. Metadata Region
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
    # 4. Body Composition Area
    # ------------------------------------------------------
    st.markdown("### 📝 Draft Article Text")
    st.caption("For full structured writing tools, go to the Write tab.")

    st.text_area(
        "Compose Here",
        key="design_body",
        height=300,
    )

    # ------------------------------------------------------
    # 5. NEW — SEND METADATA TO WRITE TAB
    # ------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🔄 Send Metadata to Write Tab")

    if st.button("➡️ Send to Write Tab (Safe Mode)"):

        incoming_data = {
            "title": st.session_state.get("design_title", ""),
            "summary": st.session_state.get("design_summary", ""),
            "source": st.session_state.get("design_source", ""),
            "timestamp": st.session_state.get("design_timestamp", ""),
            "author": st.session_state.get("design_author", ""),
            "url": st.session_state.get("design_url", ""),
            "body": st.session_state.get("design_body", ""),
        }

        try:
            # Load and update state buffer
            write_state = WriteState.load()
            write_state.yaml_buffer = incoming_data
            write_state.last_saved_name = "(Design→Write)"
            write_state.save()

            st.success("📨 Metadata sent to Write Tab (pending import).")
            st.info("Switch to the Write tab → You will see 'YAML Incoming'.")

        except Exception as e:
            st.error(f"Failed to stage metadata: {e}")

    # ------------------------------------------------------
    # 6. YAML LOAD + SAVE (Normal)
    # ------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📦 Save / Load Article as YAML")

    yaml_files = get_yaml_options()
    selected_yaml = st.selectbox("Load existing YAML", ["(None)"] + yaml_files)

    col1, col2 = st.columns(2)

    # LOAD YAML
    with col1:
        if selected_yaml != "(None)":
            if st.button("Load YAML"):
                try:
                    data = load_yaml(selected_yaml)

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

    # SAVE YAML
    with col2:

        filename = st.text_input(
            "Filename (e.g., article1.yaml)",
            key="design_save_name",
            value="article_draft.yaml",
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

                    write_state = WriteState.load()
                    write_state.yaml_buffer = data
                    write_state.last_saved_name = filename
                    write_state.save()

                    st.success(f"Saved: {filename}")
                    st.info("📨 YAML staged for Write Tab (safe mode).")

                except Exception as e:
                    st.error(f"Save failed: {e}")

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------
    st.markdown("---")
    st.success("Design tab ready. Click headlines in Monitor to send more stories.")
