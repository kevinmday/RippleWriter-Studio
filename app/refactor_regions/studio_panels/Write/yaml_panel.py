# ==========================================================
#  RippleWriter Studio â€” Write Tab
#  YAML Panel (Receiver + Editor)
# ==========================================================

import streamlit as st
import yaml

from app.utils.yaml_tools import (
    save_yaml,
    load_yaml,
    list_yaml_files
)

from app.refactor_regions.studio_state.write_state import WriteState


# ----------------------------------------------------------
# Helper â€” Pretty YAML
# ----------------------------------------------------------
def pretty_yaml(data: dict) -> str:
    return yaml.dump(data, sort_keys=False, allow_unicode=True)


# ----------------------------------------------------------
# YAML Panel (Write Tab)
# ----------------------------------------------------------
def render_yaml_panel(state: WriteState):
    """
    YAML Editor Panel for the Write Tab.

    - Receives YAML data from Design tab via:
        st.session_state["incoming_yaml"]

    - Updates:
        state.yaml_data
    """

    st.markdown("### ðŸ—‚ï¸ YAML Structure Editor")

    # ------------------------------------------------------
    # PRIORITY INPUT: YAML sent from Design Tab
    # ------------------------------------------------------
    incoming = st.session_state.get("incoming_yaml")

    if incoming is not None:
        # Design tab overrides current YAML
        state.yaml_data = incoming
        del st.session_state["incoming_yaml"]

    # Use whatever is currently in WriteState
    yaml_data = state.yaml_data or {}

    # ------------------------------------------------------
    # Editor Text Area
    # ------------------------------------------------------
    yaml_text = st.text_area(
        "Full YAML",
        pretty_yaml(yaml_data),
        height=500,
        key="yaml_editor_write",
    )

    # Parse safely
    try:
        parsed = yaml.safe_load(yaml_text) or {}
        yaml_valid = True
    except Exception as e:
        yaml_valid = False
        st.error(f"YAML syntax error: {e}")

    # ------------------------------------------------------
    # Save back into state
    # ------------------------------------------------------
    if yaml_valid:
        state.yaml_data = parsed

    st.markdown("---")

    # ------------------------------------------------------
    # Save to Disk
    # ------------------------------------------------------
    st.subheader("Save Draft")

    draft_files = list_yaml_files()
    default_name = state.last_saved_name or (
        draft_files[0] if draft_files else "draft.yaml"
    )

    filename = st.text_input(
        "Filename",
        value=default_name,
        key="yaml_save_filename"
    )

    if st.button("ðŸ’¾ Save YAML", key="yaml_save_btn"):
        if not filename.endswith(".yaml"):
            st.error("Filename must end with `.yaml`")
        else:
            save_yaml(filename, state.yaml_data)
            state.last_saved_name = filename
            st.success(f"Saved as **{filename}**")

