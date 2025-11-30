# ==========================================================
# RippleWriter Studio — WRITE PANEL 2.1 (Non-Blocking Version)
# • Safe full-metadata import gate (Option B)
# • Never overwrites drafts without user action
# • No st.stop() — does NOT block other tabs
# • Snapshot + action buttons + red alert banner
# ==========================================================

import streamlit as st
import yaml
from datetime import datetime

from app.refactor_regions.studio_state.write_state import WriteState
from app.utils.yaml_tools import (
    list_templates,
    load_template,
    load_model
)

# ----------------------------------------------------------
# YAML IMPORT GATE — NON-BLOCKING
# ----------------------------------------------------------
def render_yaml_import_gate(state: WriteState):
    """Displays the blocking UI for metadata import — WITHOUT st.stop()."""

    st.markdown("---")

    # RED high-alert banner
    st.markdown(
        """
        <div style="
            background-color:#6e1f1f;
            border:1px solid #aa4c4c;
            padding:18px;
            border-radius:6px;
            text-align:center;
            color:#fff;
            font-weight:600;
            font-size:16px;">
            ⚠️ ACTION REQUIRED  
            <br>Incoming full metadata transfer from the Design tab.
            <br><span style='opacity:0.8;'>The Write Panel is locked — use the action buttons <b>below</b> to continue.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # View incoming YAML block
    with st.expander("📄 View Incoming Metadata (YAML)", expanded=False):
        st.code(
            yaml.dump(state.yaml_buffer, allow_unicode=True, sort_keys=False),
            language="yaml"
        )

    # Snapshot of what user currently has
    st.subheader("📰 Current Write Panel Snapshot (Before Import)")
    st.write(
        f"**Title:** {state.title or ''}\n"
        f"**Deck:** {state.deck or ''}\n"
        f"**Author:** {state.author or ''}\n"
        f"**Source:** {state.source or ''}\n"
        f"**Timestamp:** {state.timestamp or ''}\n"
        f"**URL:** {state.url or ''}\n"
    )

    st.markdown("---")

    colA, colB = st.columns([1, 1])

    # IMPORT BUTTON (overwrite)
    with colA:
        if st.button("🔻 IMPORT METADATA (Overwrite Everything)", type="primary"):
            incoming = state.yaml_buffer

            # Apply incoming metadata
            state.title = incoming.get("title", "")
            state.deck = incoming.get("summary", "")
            state.source = incoming.get("source", "")
            state.timestamp = incoming.get("timestamp", "")
            state.author = incoming.get("author", "")
            state.url = incoming.get("url", "")
            state.draft_text = incoming.get("body", "")

            state.yaml_text = yaml.dump(incoming, allow_unicode=True, sort_keys=False)
            state.yaml_buffer = {}
            state.write_dirty = False
            state.save()

            st.success("Metadata imported into Write Panel.")
            st.session_state["write_gate_resolved"] = True

    # IGNORE BUTTON
    with colB:
        if st.button("❌ Ignore Incoming Metadata"):
            state.yaml_buffer = {}
            state.save()
            st.info("Incoming metadata discarded.")
            st.session_state["write_gate_resolved"] = True

    # 👇 RETURN so the rest of the Write Panel does not render
    return True  # “Write Panel is locked” flag


# ----------------------------------------------------------
# MAIN WRITE PANEL
# ----------------------------------------------------------
def render_write_panel():

    state = WriteState.load()

    # Prevent showing partial UI when gate is active
    gate_resolved = st.session_state.get("write_gate_resolved", False)

    # ------------------------------------------------------
    # 1. Handle import gate
    # ------------------------------------------------------
    if state.yaml_buffer and not gate_resolved:
        locked = render_yaml_import_gate(state)
        if locked:
            return  # <-- NON-BLOCKING EXIT (only exits Write Panel)

   
    # Reset gate flag safely — only when no YAML is waiting
    if not state.yaml_buffer:
        st.session_state["write_gate_resolved"] = False


    # ------------------------------------------------------
    # 2. Header
    # ------------------------------------------------------
    st.title("✍️ Write Panel")
    st.caption("Full-width writing environment — safe-edit, full metadata.")
    st.markdown("---")

    # ------------------------------------------------------
    # 3. Load resources
    # ------------------------------------------------------
    template_files = list_templates()
    template_names = [p.name for p in template_files]

    equations = load_model("equations.yaml")
    intention = load_model("intention.yaml")

    # ------------------------------------------------------
    # 4. Template selector
    # ------------------------------------------------------
    st.subheader("Document Template")

    selected_tpl = st.selectbox(
        "Choose Template",
        ["(none selected)"] + template_names
    )

    selected_template = (
        load_template(selected_tpl)
        if selected_tpl in template_names
        else None
    )

    st.markdown("---")

    # ------------------------------------------------------
    # 5. FULL METADATA INPUT (Option B)
    # ------------------------------------------------------
    st.subheader("Metadata (Full)")

    colA, colB = st.columns(2)

    with colA:
        new_title = st.text_input("Headline", value=state.title, key="write_title")
        new_deck = st.text_input("Summary / Deck", value=state.deck, key="write_deck")
        new_author = st.text_input("Author", value=state.author, key="write_author")

    with colB:
        new_source = st.text_input("Source", value=state.source, key="write_source")
        new_timestamp = st.text_input("Timestamp", value=state.timestamp, key="write_timestamp")
        new_url = st.text_input("Source URL", value=state.url, key="write_url")

    # Save metadata changes
    fields_changed = (
        new_title != state.title or
        new_deck != state.deck or
        new_author != state.author or
        new_source != state.source or
        new_timestamp != state.timestamp or
        new_url != state.url
    )

    if fields_changed:
        state.title = new_title
        state.deck = new_deck
        state.author = new_author
        state.source = new_source
        state.timestamp = new_timestamp
        state.url = new_url
        state.write_dirty = True
        state.save()

    st.markdown("---")

    # ------------------------------------------------------
    # 6. Template YAML block
    # ------------------------------------------------------
    with st.expander("📄 View Template YAML Block", expanded=False):
        if selected_template:
            st.json(selected_template)
        else:
            st.info("No template selected.")

    st.markdown("---")

    # ------------------------------------------------------
    # 7. Draft Editor
    # ------------------------------------------------------
    st.subheader("Draft Editor")

    updated_draft = st.text_area(
        "Write or Edit Draft",
        value=state.draft_text,
        height=350,
        key="write_draft"
    )

    if updated_draft != state.draft_text:
        state.draft_text = updated_draft
        state.write_dirty = True
        state.save()

    st.markdown("---")

    # ------------------------------------------------------
    # 8. Generate From Template
    # ------------------------------------------------------
    st.subheader("AI Writer")

    if st.button("✨ Generate Draft From Template"):
        if not selected_template:
            st.error("No template selected.")
        else:
            sections = selected_template.get("sections", [])
            outline = "\n\n".join([f"## {s}" for s in sections])

            generated = (
                f"# {state.title}\n\n"
                f"### {state.deck}\n\n"
                f"{outline}"
            )

            state.draft_text = generated
            state.write_dirty = True
            state.save()

            st.success("Draft generated from template.")
            st.text_area("Generated Output", generated, height=350)

    st.markdown("---")


# ============================================================
# 📸 Screenshot / Image Uploader Panel
# ============================================================

st.markdown("### 📸 Add Images / Screenshots")
st.caption("Attach screenshots, captured evidence, or visual context. Metadata auto-included in YAML.")

with st.container(border=True):
    colA, colB = st.columns([2, 1])

    with colA:
        uploaded_image = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=False
        )

        if uploaded_image:
            st.success(f"Uploaded: **{uploaded_image.name}**")

    with colB:
        if uploaded_image:
            st.image(uploaded_image, caption="Preview", use_container_width=True)
        else:
            st.info("No image uploaded yet.")

# Save reference for YAML export
if uploaded_image:
    st.session_state["uploaded_image"] = uploaded_image



    # ------------------------------------------------------
    # 9. HTML Preview
    # ------------------------------------------------------
    st.subheader("Live Preview (HTML)")

    safe = state.draft_text.replace("\n", "<br>")
    html_preview = (
        f"<h1>{state.title}</h1>"
        f"<h3>{state.deck}</h3>"
        f"<p><b>Source:</b> {state.source}<br>"
        f"<b>Timestamp:</b> {state.timestamp}<br>"
        f"<b>Author:</b> {state.author}<br>"
        f"<b>URL:</b> {state.url}</p>"
        f"<p>{safe}</p>"
    )

    st.markdown(html_preview, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Write Panel — Full-Metadata + Safe-Edit (v2.1 Non-Blocking)")
