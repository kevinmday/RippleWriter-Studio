# ==========================================================
#  RippleWriter Studio — Write Tab
#  YAML Panel (Receiver + Editor)
# ==========================================================

import streamlit as st
import yaml

from app.utils.yaml_tools import save_yaml, load_yaml, list_yaml_files
from app.refactor_regions.studio_state.write_state import WriteState


# ----------------------------------------------------------
# Helper
# ----------------------------------------------------------
def pretty_yaml(data: dict) -> str:
    return yaml.dump(data, sort_keys=False, allow_unicode=True)


# ----------------------------------------------------------
# Main Render
# ----------------------------------------------------------
def render_yaml_panel(state):
    """
    YAML Editor Panel for the Write Tab.
    Receives YAML from the Design Tab via session_state["incoming_yaml"].
    Updates WriteState.yaml_data accordingly.
    """

    st.markdown("### 🧩 YAML Structure Editor")

    # ------------------------------------------------------
    # PRIORITY INPUT: YAML sent from Design Tab
    # ------------------------------------------------------
    if "incoming_yaml" in st.session_state:
        try:
            parsed = yaml.safe_load(st.session_state["incoming_yaml"]) or {}
            state.yaml_data = parsed
            st.success("YAML loaded from Design Tab.")
        except Exception as e:
            st.error(f"Failed to parse YAML sent from Design tab: {e}")

        # Clear after ingestion so it doesn't reapply
        del st.session_state["incoming_yaml"]

    # ------------------------------------------------------
    # INITIAL YAML LOAD (if empty)
    # ------------------------------------------------------
    if not state.yaml_data:
        st.info("YAML structure is currently empty.")
        yaml_text_initial = ""
    else:
        yaml_text_initial = pretty_yaml(state.yaml_data)

    # ------------------------------------------------------
    # YAML Editor Text Area
    # ------------------------------------------------------
    yaml_text = st.text_area(
        "Edit YAML",
        value=yaml_text_initial,
        height=400,
        key="write_yaml_editor",
    )

    # ------------------------------------------------------
    # Parse user edits
    # ------------------------------------------------------
    parse_error = None
    try:
        updated_yaml = yaml.safe_load(yaml_text) or {}
    except Exception as e:
        updated_yaml = None
        parse_error = str(e)

    if parse_error:
        st.error(f"YAML parsing error: {parse_error}")
    else:
        state.yaml_data = updated_yaml

    # ------------------------------------------------------
    # Save Controls
    # ------------------------------------------------------
    st.markdown("---")
    st.subheader("Save YAML File")

    # list YAML files for save-as convenience
    drafts = list_yaml_files()

    default_name = (
        state.current_yaml_file
        if getattr(state, "current_yaml_file", None)
        else ("draft.yaml" if not drafts else drafts[0])
    )

    filename = st.text_input(
        "Save as filename",
        value=default_name,
        key="yaml_save_name",
    )

    # Save Button
    if st.button("💾 Save YAML Draft", key="write_yaml_save_btn"):
        if not filename.endswith(".yaml"):
            st.error("Filename must end with .yaml")
        else:
            save_yaml(filename, state.yaml_data)
            state.current_yaml_file = filename
            st.success(f"Saved YAML draft as {filename}")

    # ------------------------------------------------------
    # Footer
    # ------------------------------------------------------
    st.caption("YAML Editor — All structure-level work happens here.")
