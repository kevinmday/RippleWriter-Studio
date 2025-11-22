import yaml
import streamlit as st

# ----------------------------------------------------------
# WRITE ENGINE — Processes all WriteState flags
# ----------------------------------------------------------

def process_write_engine(state):
    """
    Central processor for Write Tab actions.
    Every flag set by the UI is handled here.
    """

    # ------------------------------------------------------
    # 1. Generate Draft Structure
    # ------------------------------------------------------
    if state.generate_structure_flag:
        state.yaml_text = generate_structure(state.draft_text)
        state.generate_structure_flag = False

    # ------------------------------------------------------
    # 2. Write & Render Pipeline
    # ------------------------------------------------------
    if state.write_render_flag:
        new_draft, new_yaml = write_and_render(state.draft_text)
        state.draft_text = new_draft
        state.yaml_text = new_yaml
        state.write_render_flag = False

    # ------------------------------------------------------
    # 3. Rewrite Section
    # ------------------------------------------------------
    if state.rewrite_section_flag:
        if state.selected_section:
            state.draft_text = rewrite_section_logic(
                state.draft_text,
                state.selected_section
            )
        state.rewrite_section_flag = False

    # ------------------------------------------------------
    # 4. YAML -> HTML Preview
    # ------------------------------------------------------
    if state.preview_flag:
        state.rendered_html = generate_preview_html(state.yaml_text)
        state.preview_flag = False

    # ------------------------------------------------------
    # 5. Load YAML from file
    # ------------------------------------------------------
    if state.load_yaml_flag:
        try:
            with open(f"{state.current_doc}.yaml", "r") as f:
                state.yaml_text = f.read()
        except Exception as e:
            st.error(f"Load error: {e}")
        state.load_yaml_flag = False

    # ------------------------------------------------------
    # 6. Save YAML
    # ------------------------------------------------------
    if state.save_yaml_flag:
        try:
            with open(f"{state.current_doc}.yaml", "w") as f:
                f.write(state.yaml_text)
            st.success("YAML saved.")
        except Exception as e:
            st.error(f"Save error: {e}")
        state.save_yaml_flag = False

    # ------------------------------------------------------
    # 7. Export HTML
    # ------------------------------------------------------
    if state.export_flag:
        try:
            with open(f"{state.current_doc}.html", "w") as f:
                f.write(state.rendered_html or "")
            st.success("HTML exported.")
        except Exception as e:
            st.error(f"Export error: {e}")
        state.export_flag = False

    # ------------------------------------------------------
    # 8. Structural Additions
    # ------------------------------------------------------
    if state.add_section_flag:
        state.yaml_text = add_section_to_yaml(state.yaml_text)
        state.add_section_flag = False

    if state.add_pullquote_flag:
        state.yaml_text = add_pullquote_to_yaml(state.yaml_text)
        state.add_pullquote_flag = False

    if state.add_factbox_flag:
        state.yaml_text = add_factbox_to_yaml(state.yaml_text)
        state.add_factbox_flag = False

    if state.add_image_flag:
        state.yaml_text = add_image_to_yaml(state.yaml_text)
        state.add_image_flag = False

    return state


# ----------------------------------------------------------
# Helper Logic Functions (placeholders)
# ----------------------------------------------------------

def generate_structure(draft_text):
    return yaml.safe_dump({
        "title": "Untitled Draft",
        "deck": "",
        "tags": [],
        "sections": [
            {"heading": "Introduction", "content": draft_text[:200] + "..."},
            {"heading": "Main Analysis", "content": "..."},
            {"heading": "Conclusion", "content": "..."}
        ]
    }, sort_keys=False)

def write_and_render(draft_text):
    rendered = draft_text + "\n\n[Rendered output placeholder]"
    yaml_out = generate_structure(draft_text)
    return rendered, yaml_out

def rewrite_section_logic(draft_text, section_name):
    return draft_text.replace(
        section_name,
        section_name + " (rewritten via engine)"
    )

def generate_preview_html(yaml_text):
    # Placeholder until NYT-style renderer
    return f"<html><body><pre>{yaml_text}</pre></body></html>"

def add_section_to_yaml(yaml_text):
    data = yaml.safe_load(yaml_text) or {}
    data.setdefault("sections", []).append({"heading": "New Section", "content": "..."})
    return yaml.safe_dump(data, sort_keys=False)

def add_pullquote_to_yaml(yaml_text):
    data = yaml.safe_load(yaml_text) or {}
    data.setdefault("pull_quotes", []).append("New pull quote")
    return yaml.safe_dump(data, sort_keys=False)

def add_factbox_to_yaml(yaml_text):
    data = yaml.safe_load(yaml_text) or {}
    data.setdefault("fact_boxes", []).append({"title": "New Fact", "content": "..."})
    return yaml.safe_dump(data, sort_keys=False)

def add_image_to_yaml(yaml_text):
    data = yaml.safe_load(yaml_text) or {}
    data.setdefault("images", []).append({"src": "image.png", "caption": "Image caption"})
    return yaml.safe_dump(data, sort_keys=False)
