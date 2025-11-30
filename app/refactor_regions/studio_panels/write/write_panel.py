# =====================================================================
# RippleWriter Studio — WRITE PANEL v2.5 (Stable Edition)
# • Fully compact layout
# • No giant empty spaces (dev or cloud)
# • Fixed container stretch bug
# • Clean uploader (thumbnail)
# • Always renders Preview section
# • Non-blocking YAML import gate
# =====================================================================

import streamlit as st
import yaml
from datetime import datetime

from app.refactor_regions.studio_state.write_state import WriteState
from app.utils.yaml_tools import (
    list_templates,
    load_template,
    load_model
)

# =====================================================================
# GLOBAL CSS — TIGHT LAYOUT, ZERO EMPTY SPACE
# =====================================================================
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }

        /* Compress vertical spacing across all widgets */
        .stTextInput, .stSelectbox, .stTextArea, .stFileUploader {
            margin-bottom: 0rem !important;
            padding-bottom: 0rem !important;
        }

        h1, h2, h3 {
            margin-top: 0.4rem !important;
            margin-bottom: 0.4rem !important;
        }

        .stMarkdown {
            margin-top: 0.2rem !important;
            margin-bottom: 0.2rem !important;
        }

        hr {
            margin-top: 0.4rem !important;
            margin-bottom: 0.4rem !important;
        }

        /* Prevent container auto-stretch (THIS FIXES THE BLANK SPACE) */
        .stContainer {
            flex-grow: 0 !important;
        }

        /* Collapse expander spacing */
        .streamlit-expanderHeader {
            margin-top: 0.1rem !important;
            margin-bottom: 0.1rem !important;
        }

        /* Reduce uploader dropzone vertical size */
        .stFileUploader > div {
            padding-top: 0.2rem !important;
            padding-bottom: 0.2rem !important;
        }

    </style>
""", unsafe_allow_html=True)



# =====================================================================
# YAML IMPORT GATE — NON-BLOCKING
# =====================================================================
def render_yaml_import_gate(state: WriteState):

    st.markdown("---")

    st.markdown("""
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
            <br><span style='opacity:0.8;'>Use the action buttons below.</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📄 View Incoming YAML"):
        st.code(yaml.dump(state.yaml_buffer, allow_unicode=True, sort_keys=False), language="yaml")

    st.subheader("📰 Current Write Panel Snapshot")

    st.write(
        f"**Title:** {state.title}\n"
        f"**Deck:** {state.deck}\n"
        f"**Author:** {state.author}\n"
        f"**Source:** {state.source}\n"
        f"**Timestamp:** {state.timestamp}\n"
        f"**URL:** {state.url}\n"
    )

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:
        if st.button("🔻 IMPORT METADATA (Overwrite All)", type="primary"):
            inc = state.yaml_buffer

            state.title     = inc.get("title", "")
            state.deck      = inc.get("summary", "")
            state.source    = inc.get("source", "")
            state.timestamp = inc.get("timestamp", "")
            state.author    = inc.get("author", "")
            state.url       = inc.get("url", "")
            state.draft_text = inc.get("body", "")

            state.yaml_text = yaml.dump(inc, allow_unicode=True, sort_keys=False)
            state.yaml_buffer = {}
            state.write_dirty = False
            state.save()

            st.success("Metadata imported.")
            st.session_state["write_gate_resolved"] = True

    with colB:
        if st.button("❌ Ignore Incoming Metadata"):
            state.yaml_buffer = {}
            state.save()
            st.info("Metadata discarded.")
            st.session_state["write_gate_resolved"] = True

    return True




# =====================================================================
# MAIN WRITE PANEL
# =====================================================================
def render_write_panel():

    state = WriteState.load()
    gate_resolved = st.session_state.get("write_gate_resolved", False)

    # ------------------------------
    # Handle YAML Gate
    # ------------------------------
    if state.yaml_buffer and not gate_resolved:
        if render_yaml_import_gate(state):
            return

    if not state.yaml_buffer:
        st.session_state["write_gate_resolved"] = False


    # ------------------------------
    # HEADER
    # ------------------------------
    st.title("✍️ Write Panel")
    st.caption("Full-width writing environment — with compact layout.")
    st.markdown("---")


    # ------------------------------
    # LOAD TEMPLATES + MODELS
    # ------------------------------
    template_files = list_templates()
    template_names = [p.name for p in template_files]

    equations = load_model("equations.yaml")
    intention = load_model("intention.yaml")


    # ------------------------------
    # TEMPLATE SELECTOR
    # ------------------------------
    st.subheader("Document Template")

    selected_tpl = st.selectbox(
        "Choose Template",
        ["(none selected)"] + template_names
    )

    selected_template = (
        load_template(selected_tpl)
        if selected_tpl in template_names else None
    )

    st.markdown("---")


    # ------------------------------
    # METADATA INPUTS
    # ------------------------------
    st.subheader("Metadata (Full)")

    colA, colB = st.columns(2)

    with colA:
        t = st.text_input("Headline", value=state.title)
        d = st.text_input("Summary / Deck", value=state.deck)
        a = st.text_input("Author", value=state.author)

    with colB:
        s  = st.text_input("Source", value=state.source)
        ts = st.text_input("Timestamp", value=state.timestamp)
        u  = st.text_input("Source URL", value=state.url)

    if (t, d, a, s, ts, u) != (state.title, state.deck, state.author, state.source, state.timestamp, state.url):
        state.title, state.deck, state.author = t, d, a
        state.source, state.timestamp, state.url = s, ts, u
        state.write_dirty = True
        state.save()

    st.markdown("---")


    # ------------------------------
    # TEMPLATE YAML PREVIEW
    # ------------------------------
    with st.expander("📄 View Template YAML"):
        if selected_template:
            st.json(selected_template)
        else:
            st.info("No template selected.")

    st.markdown("---")


    # ------------------------------
    # DRAFT EDITOR
    # ------------------------------
    st.subheader("Draft Editor")

    updated = st.text_area(
        "Write or Edit Draft",
        value=state.draft_text,
        height=320
    )

    if updated != state.draft_text:
        state.draft_text = updated
        state.write_dirty = True
        state.save()

    st.markdown("---")


    # ------------------------------
    # AI WRITER
    # ------------------------------
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

            st.success("Draft generated.")
            st.text_area("Generated Output", generated, height=320)

    st.markdown("---")


    # =================================================================
    # SCREENSHOT UPLOADER — FINAL FIX (NO EMPTY SPACE)
    # =================================================================
    st.subheader("📸 Add Images / Screenshots")
    st.caption("Attach a small image or screenshot. Metadata will be included during export.")

    # FIX: do NOT wrap in st.container() (this is what caused giant blank space)
    colX, colY = st.columns([2, 1], vertical_alignment="top")

    with colX:
        uploaded_image = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=False
        )

        if uploaded_image:
            st.success(f"Uploaded: {uploaded_image.name}")

    with colY:
        if uploaded_image:
            st.image(uploaded_image, caption="Preview", width=200)
        else:
            st.info("No image.")

    if uploaded_image:
        st.session_state["uploaded_image"] = uploaded_image

    st.markdown("---")


    # =================================================================
    # HTML PREVIEW — ALWAYS RENDERS
    # =================================================================
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
    st.caption("Write Panel v2.5 — Stable, Compact, No-Whitespace Edition")
