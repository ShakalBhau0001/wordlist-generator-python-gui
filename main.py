from __future__ import annotations

import streamlit as st

from gui import about, instructions, wordlist

st.set_page_config(
    page_title="Wordlist Generator",
    page_icon="🔐",
    layout="centered",
)
st.title("🔐 Wordlist Generator 🔐")
st.caption("Targeted, personal-info-based wordlist generation.")
tab_wordlist, tab_instructions, tab_about = st.tabs(
    ["📝 Wordlist", "📘 Instructions", "ℹ️ About"]
)

with tab_wordlist:
    wordlist.render()

with tab_instructions:
    instructions.render()

with tab_about:
    about.render()
