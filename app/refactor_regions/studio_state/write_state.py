import streamlit as st
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class WriteState:
    """
    Unified state manager for the Write Tab.
    Loaded/saved through Streamlit session state.
    """

    # -----------------------------------------
    # Core Article Fields
    # -----------------------------------------
    current_doc: str = None
    title: str = ""
    deck: str = ""
    tags: List[str] = field(default_factory=list)
    status: str = "Draft"

    # -----------------------------------------
    # Draft + YAML text
    # -----------------------------------------
    draft_text: str = ""
    yaml_text: str = ""

    # -----------------------------------------
    # Section selection (future feature)
    # -----------------------------------------
    selected_section: Optional[str] = None

    # -----------------------------------------
    # Action Flags (Write Engine)
    # -----------------------------------------
    generate_structure_flag: bool = False
    write_render_flag: bool = False
    rewrite_section_flag: bool = False
    preview_flag: bool = False

    # -----------------------------------------
    # File Actions
    # -----------------------------------------
    save_yaml_flag: bool = False
    load_yaml_flag: bool = False
    export_flag: bool = False

    # -----------------------------------------
    # Structure Additions
    # -----------------------------------------
    add_section_flag: bool = False
    add_pullquote_flag: bool = False
    add_factbox_flag: bool = False
    add_image_flag: bool = False

    # -----------------------------------------
    # Validation
    # -----------------------------------------
    validate_flag: bool = False

    # -----------------------------------------
    # Sync methods for Streamlit state
    # -----------------------------------------
    @staticmethod
    def load():
        """Load from st.session_state or create a new instance."""
        if "write_state" not in st.session_state:
            st.session_state.write_state = WriteState()
        return st.session_state.write_state

    def save(self):
        """Commit this state back into session_state."""
        st.session_state.write_state = self
