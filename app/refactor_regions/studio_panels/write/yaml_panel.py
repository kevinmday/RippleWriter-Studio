# ==========================================================
#  RippleWriter Studio — Write Tab (2025 Modular Build)
#  YAML Panel (Receiver + Editor) — Option B Safe Mode
# ==========================================================

import streamlit as st
import yaml

from app.utils.yaml_tools import (
    save_yaml,
    list_yaml_files
)

from app.refactor_regions.studio_state.write_state import WriteState


# ----------------------------------------------------------
# Pretty YAML helper
# ----------------------------------------------------------
def pretty_yaml(data: dict) -> str:
    return yaml.dump(
        data,
        sort_keys=False,
        allow_unicode=True
    )


# ----------------------------------------------------------
# YAML Editor Panel (Safe Import Mode)
# ----------------------------------------------------------
def render_yaml_panel(state: WriteState):
    """
    YAML Editor Panel for the Write Tab.
    Option B safety rules:
      - YAML received from Design goes into state.yaml_buffer
      - DOES NOT overwrite write panel fields automatically
      - User must click an Import button in Write Panel to apply
    """

    st.markdown("### 🧩 YAML Structure Editor (Safe Mode)")
    st.caption("YAML changes no longer overwrite Write Panel automatically.")

    # ------------------------------------------------------
    # 1. RECEIVE YAML FROM DESIGN TAB (but do NOT apply it)
    # ------------------------------------------------------
    incoming = st.session_state.get("incoming_yaml")

    if incoming is not None:
        try:
            parsed = yaml.safe_load(incoming) or {}

            # Store for later manual import
            state.yaml_buffer = parsed

            st.success("YAML received from Design Tab and stored safely.")
        except Exception as e:
            st.error(f"Failed to parse incoming YAML: {e}")

        # Remove so it doesn't re-process
        del st.session_state["incoming_yaml"]

    # ------------------------------------------------------
    # 2. JSON/YAML shown in editor comes from buffer, NOT write panel
    # ------------------------------------------------------
    buffer_yaml = state.yaml_buffer or {}
    editor_initial_text = pretty_yaml(buffer_yaml)

    yaml_text = st.text_area(
        label="YAML Buffer (Edit Safely)",
        value=editor_initial_text,
        height=500,
        key="yaml_editor_buffer",
    )

    # ------------------------------------------------------
    # 3. Parse user edits into yaml_buffer (safe)
    # ------------------------------------------------------
    parse_error = None
    try:
        parsed_yaml = yaml.safe_load(yaml_text) or {}
    except Exception as e:
        parse_error = str(e)
        parsed_yaml = None

    if parse_error:
        st.error(f"YAML parsing error: {parse_error}")
    else:
        # Update buffer safely
        state.yaml_buffer = parsed_yaml

    st.markdown("---")

    # ------------------------------------------------------
    # 4. SAVE YAML BUFFER TO DISK
    # ------------------------------------------------------
    st.subheader("Save YAML Draft")

    draft_files = list_yaml_files()
    default_name = (
        state.last_saved_name
        if state.last_saved_name
        else (draft_files[0] if draft_files else "draft.yaml")
    )

    filename = st.text_input(
        "Filename",
        value=default_name,
        key="yaml_save_filename"
    )

    if st.button("💾 Save YAML", key="yaml_save_btn"):
        if not filename.endswith(".yaml"):
            st.error("Filename must end with `.yaml`")
        else:
            try:
                save_yaml(filename, state.yaml_buffer)
                state.last_saved_name = filename
                st.success(f"Saved YAML to **{filename}**")
            except Exception as e:
                st.error(f"Failed to save YAML: {e}")

    st.caption("NOTE: Use the Write Panel to import YAML into active draft.")

