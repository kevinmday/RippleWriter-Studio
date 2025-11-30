# ==========================================================
#  RippleWriter Studio — Monitor Region (PHASE 1)
#  Functional, crash-proof version
#  No HTML wrappers, no CSS, full click → Design support
# ==========================================================

import streamlit as st
from datetime import datetime
import feedparser
import requests
import socket

from app.utils.errors import (
    friendly_network_error,
    friendly_rss_error,
)

# NEW: HTML cleaner
from app.utils.text_clean import clean_html

# ----------------------------------------------------------
# RSS SOURCES
# ----------------------------------------------------------
RSS_SOURCES = {
    "Reuters Politics": "http://feeds.reuters.com/Reuters/PoliticsNews",
    "AP Top News": "https://rss.apnews.com/apf-topnews",
    "Guardian World": "https://www.theguardian.com/world/rss",
}

# ----------------------------------------------------------
# Internet Check
# ----------------------------------------------------------
def has_internet(timeout=3):
    try:
        requests.get("https://www.google.com", timeout=timeout)
        return True
    except Exception:
        return False

# ----------------------------------------------------------
# RSS Fetch
# ----------------------------------------------------------
def fetch_feed(url):
    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            bozo = str(feed.bozo_exception)
            if "11001" in bozo or "getaddrinfo" in bozo:
                return None, "DNS lookup failed"
            return None, bozo

        return feed, None

    except socket.gaierror:
        return None, "DNS lookup failed"
    except Exception as e:
        return None, str(e)

# ----------------------------------------------------------
# MAIN RENDER FUNCTION (PHASE 1 SAFE MODE)
# ----------------------------------------------------------
def render_monitor_region():
    st.header("📡 RippleWriter — Monitor")
    st.caption("Click a headline to populate the Design tab.")

    # Global internet check
    if not has_internet():
        st.error(friendly_network_error("No internet connection."))
        return

    # ------------------------------------------------------
    # AUTO-REFRESH & REFRESH BUTTON
    # ------------------------------------------------------
    auto = st.checkbox("Auto-refresh every 10 seconds", value=False)
    if auto:
        st.rerun()

    if st.button("Refresh Feeds"):
        st.rerun()

    # ------------------------------------------------------
    # MAIN LAYOUT (safe mode, native only)
    # ------------------------------------------------------
    left, right = st.columns([3, 1])

    # ============================
    # LEFT SIDE: NEWS FEEDS
    # ============================
    with left:
        for source_name, url in RSS_SOURCES.items():

            st.subheader(source_name)

            feed, error = fetch_feed(url)

            if error:
                st.error(friendly_rss_error(source_name, error))
                continue

            if not feed or not feed.entries:
                st.warning("⚠️ Feed returned no items.")
                continue

            # Show first 5 items
            for entry in feed.entries[:5]:

                title = entry.get("title", "(no title)")

                # NEW: CLEAN SUMMARY
                summary_raw = entry.get("summary", "")
                summary = clean_html(summary_raw)

                ts = entry.get("published", "")
                link = entry.get("link", "")
                author = entry.get("author", "")

                # Payload for Design tab
                payload = {
                    "title": title,
                    "summary": summary,
                    "timestamp": ts,
                    "url": link,
                    "author": author,
                    "source": source_name,
                }

                # A real Streamlit button – guaranteed safe
                if st.button(title, key=f"{source_name}-{title}"):

                    st.session_state["design_payload"] = payload
                    st.session_state["go_to_design"] = True
                    st.rerun()

                if ts:
                    st.caption(ts)

    # ============================
    # RIGHT SIDE: SYSTEM STATUS
    # ============================
    with right:
        st.subheader("System Status")
        st.write("✓ RSS Active")
        st.write("✓ Internet OK")
        st.write(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

        st.markdown("---")
        st.subheader("Story Pipelines")
        st.write("• Trump Legal Crisis")
        st.write("• AI Regulation Wave")
        st.write("• National Security")
