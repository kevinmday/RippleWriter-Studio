import streamlit as st

def render_left_panel(state):
    """
    Write Tab — Left Panel
    Clean, stable metadata controls:
    - No Streamlit object leakage
    - Always store primitive strings in state
    """

    st.markdown("### Metadata & Tools")

    # ------------------------------
    # Metadata Fields
    # ------------------------------

    # Title
    state.title = st.text_input(
        "Title",
        value=state.title if isinstance(state.title, str) else "",
        key="write_meta_title"
    )

    # Author
    state.author = st.text_input(
        "Author",
        value=state.author if isinstance(state.author, str) else "",
        key="write_meta_author"
    )

    # Optional: Date (if you decide to expose it)
    if hasattr(state, "date"):
        state.date = st.text_input(
            "Date",
            value=state.date if isinstance(state.date, str) else "",
            key="write_meta_date"
        )

    # ------------------------------
    # Actions
    # ------------------------------

    st.markdown("---")
    st.subheader("Actions")

    colA, colB, colC = st.columns([1, 1, 1])

    with colA:
        if st.button("Apply Template", key="write_apply_template"):
            state.apply_template = True

    with colB:
        if st.button("Send YAML to Editor", key="write_send_yaml"):
            state.send_yaml = True

    with colC:
        if st.button("Clear Draft", key="write_clear_draft"):
            state.clear_draft = True

    # Controlled spacer — prevents Streamlit from leaving strange layout gaps
    st.markdown("")
    st.markdown("")
