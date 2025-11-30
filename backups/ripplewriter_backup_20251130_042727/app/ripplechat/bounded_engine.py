# ============================================================
# RippleChat Bounded Memory Engine (Clean Version)
# Context-Aware • Local • No External API • Text-Only Output
# ------------------------------------------------------------
# PURPOSE:
#   - Lightweight offline assistant fully contained inside RWS
#   - Maintains simple memory using session_state
#   - Produces ONLY a plain-text assistant reply (NO UI)
#   - Cannot hallucinate internet facts or external data
# ============================================================

import streamlit as st


# ------------------------------------------------------------
# Ensure session memory exists
# ------------------------------------------------------------
if "bounded_memory" not in st.session_state:
    st.session_state.bounded_memory = []


# ------------------------------------------------------------
#  Core Bounded Mode LLM
# ------------------------------------------------------------
def bounded_llm(user_msg: str) -> str:
    """
    RippleChat Bounded Mode:
    - No internet
    - No external APIs
    - No markdown UI returned
    - No Streamlit chat_message rendering here
    - Pure text output only
    """

    # 1. Store user message in memory
    st.session_state.bounded_memory.append({
        "role": "user",
        "content": user_msg
    })

    # 2. Internal context note (not printed)
    _system_context = (
        "You are RippleChat (Bounded Mode) inside RippleWriter Studio. "
        "You cannot access the internet, search engines, external APIs, "
        "or external factual databases. "
        "You rely ONLY on the user's chat history and RWS tab context "
        "(Design / Write / Analyze / Export / Controls / RippleChat / Monitor)."
    )

    # 3. Build recent memory window (not printed — internal only)
    _recent_history = "\n".join([
        f"{m['role']}: {m['content']}"
        for m in st.session_state.bounded_memory[-8:]
    ])

    # 4. Compose clean text-only assistant reply
    reply = (
        "Based on your recent messages and current RippleWriter context:\n\n"
        f"{user_msg}\n\n"
        "(I am operating in bounded mode. "
        "No external facts. I use only your history and RWS context.)"
    )

    # 5. Save assistant reply to memory
    st.session_state.bounded_memory.append({
        "role": "assistant",
        "content": reply
    })

    # 6. Return text ONLY
    return reply

