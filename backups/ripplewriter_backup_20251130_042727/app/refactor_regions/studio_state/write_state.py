# ==========================================================
# RippleWriter Studio — WriteState (Upgraded Metadata Version)
# Supports full metadata transfer from Design → Write
# Safe-Edit Architecture (persistent JSON state)
# ==========================================================

import json
import os

STATE_PATH = "app/refactor_regions/studio_state/_write_state.json"


class WriteState:
    def __init__(
        self,
        title="",
        deck="",
        author="Kevin Day",

        # NEW FULL METADATA FIELDS
        source="",
        timestamp="",
        url="",
        tags="",
        status="",

        draft_text="",
        yaml_text="",

        yaml_buffer=None,
        write_dirty=False,
        last_saved_name=""
    ):
        # PRIMARY WRITING FIELDS
        self.title = title
        self.deck = deck
        self.author = author

        # ★ NEW: FULL ARTICLE METADATA FIELDS
        self.source = source
        self.timestamp = timestamp
        self.url = url
        self.tags = tags
        self.status = status

        # CORE DRAFT + YAML
        self.draft_text = draft_text
        self.yaml_text = yaml_text

        # YAML buffer from Design tab (Option B)
        self.yaml_buffer = yaml_buffer or {}

        # Safe-edit flag (protects work from overwrite)
        self.write_dirty = write_dirty

        # Last saved YAML filename
        self.last_saved_name = last_saved_name

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------
    def save(self):
        data = {
            "title": self.title,
            "deck": self.deck,
            "author": self.author,

            # Save all new metadata
            "source": self.source,
            "timestamp": self.timestamp,
            "url": self.url,
            "tags": self.tags,
            "status": self.status,

            "draft_text": self.draft_text,
            "yaml_text": self.yaml_text,
            "yaml_buffer": self.yaml_buffer,

            "write_dirty": self.write_dirty,
            "last_saved_name": self.last_saved_name,
        }

        os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)

        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ------------------------------------------------------
    # LOAD
    # ------------------------------------------------------
    @staticmethod
    def load():
        if not os.path.exists(STATE_PATH):
            return WriteState()

        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return WriteState()

        return WriteState(
            title=data.get("title", ""),
            deck=data.get("deck", ""),
            author=data.get("author", "Kevin Day"),

            source=data.get("source", ""),
            timestamp=data.get("timestamp", ""),
            url=data.get("url", ""),
            tags=data.get("tags", ""),
            status=data.get("status", ""),

            draft_text=data.get("draft_text", ""),
            yaml_text=data.get("yaml_text", ""),

            yaml_buffer=data.get("yaml_buffer", {}),
            write_dirty=data.get("write_dirty", False),
            last_saved_name=data.get("last_saved_name", "")
        )
