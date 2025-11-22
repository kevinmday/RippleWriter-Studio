import streamlit as st

def render_right_panel(state):
    """
    Write Tab — Right Panel
    Live HTML Preview
    """

    st.markdown("### Live Preview")

    if not state.draft_text.strip():
        st.info("Draft is empty. Nothing to preview.")
        return

    # Simple HTML preview for now
    html = f"""
    <div style="padding:20px; color:#ddd; font-size:1.1rem;">
        {state.draft_text.replace('\n','<br>')}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
