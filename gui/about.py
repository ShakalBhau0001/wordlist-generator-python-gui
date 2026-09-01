from __future__ import annotations

import streamlit as st


def render() -> None:
    st.markdown("## ℹ️ About")
    st.markdown(
        """
**Wordlist Generator (Streamlit GUI)** is a targeted, keyword-based
password wordlist generator built for learning how OSINT data (names,
nicknames, teams, dates) maps to candidate password guesses.

This project is a GUI re-implementation of the original
[wordlist-generator-python-cli](https://github.com/ShakalBhau0001/wordlist-generator-python-cli)
project — the same permutation, case/leetspeak variation, and
numeric-tail expansion logic, now wrapped in a Streamlit interface.

---

#### 🧱 How it's built

| Layer  | Responsibility                                             |
|--------|--------------------------------------------------------------|
| `core/` | Pure Python generation logic — token cleaning, permutation, variant expansion, length filtering. No UI code. |
| `gui/`  | Streamlit tabs (`Wordlist`, `Instructions`, `About`) that call into `core/` and render results. |
| `main.py` | Streamlit entry point — sets up the page and horizontal tabs. |

#### 🛠 Technologies used

- **Python 3**
- **Streamlit** — GUI framework
- **itertools / re / dataclasses** — core permutation & cleaning logic

---

#### 🪪 Author

**Creator: Shakal Bhau**

**GitHub: [ShakalBhau0001](https://github.com/ShakalBhau0001)**

---

#### ⚠️ Disclaimer

This project is created **for educational and learning purposes only**.

Use this tool only on systems and accounts **you own or are explicitly
authorized to test**. The author is not responsible for any misuse.
"""
    )
