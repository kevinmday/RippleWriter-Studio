import streamlit as st
import yaml

def render_center_panel(state):
    """
    Write Tab — Center Panel
    Draft Editor + YAML Editor
    """

    st.markdown("### Draft Editor")

    # Text draft
    state.draft_text = st.text_area(
        "Draft Text",
        value=state.draft_text,
        height=300
    )

    st.markdown("---")
    st.markdown("### YAML Editor")

    yaml_text = st.text_area(
        "YAML",
        value=yaml.dump(state.yaml_data, sort_keys=False),
        height=300
    )

    # Parse YAML updates
    try:
        state.yaml_data = yaml.safe_load(yaml_text) or {}
    except Exception as e:
        st.error(f"YAML error: {e}")
