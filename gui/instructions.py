from __future__ import annotations

import streamlit as st


def render() -> None:
    st.markdown("## 📘 Instructions")
    st.markdown(
        """
Follow these steps to generate a wordlist:

1. **Open the "Wordlist" tab.**
2. **Fill in the personal-info fields**
   - *First name* and *Last name* — the person's name.
   - *Nickname* and *Team / Company* — optional extra tokens.
   - *Date* — optional, in `dd/mm/yyyy`, `ddmmyyyy`, or `ddmmyy` format
    (e.g. `15/08/1995` or `15081995`). It is automatically split into
    day, month, year, and useful combined sub-tokens.
   - At least **one field** must be filled in to generate anything.
3. **Adjust the generation options** if you like:
   - **Minimum / Maximum length** — filters the final word list by
    character length.
   - **Max tokens combined per word** — how many fields get chained
    together into a single word. Keep this at `2`–`3` for most cases;
    larger values grow combinatorially and can be slow.
   - **Case variants** — adds `lower`, `UPPER`, `Capitalized`, and
    `CamelCase` forms.
   - **Leetspeak** — substitutes letters with look-alike numbers
    (`a→4`, `e→3`, `i→1`, `o→0`, `s→5`, `t→7`, `b→8`).
   - **Separators** — joins combined tokens with `-`, `_`, `.`, or
    nothing at all.
   - **Numeric tail suffixes** — appends `00`–`99` and the last 10
    years to each word.
4. **Set an output file name** (without the `.txt` extension).
5. Click **🚀 Generate wordlist**.
6. Review the **word count**, the **tokens that were used**, and a
   **preview** of the first 50 generated words.
7. Click **⬇️ Download** to save the full wordlist as a `.txt` file.

---

#### 💡 Tips

- If a configuration would create an unreasonably large number of
  combinations, the app will warn you or refuse to run — try lowering
  **Max tokens combined per word** or leaving some fields empty.
- Leetspeak and case variants multiply the word count quickly when
  combined with numeric tails — turn some off if you only need a
  smaller, focused list.
- The generated list is **de-duplicated** and **sorted alphabetically**
  automatically.

---

#### ⚠️ Responsible use

This tool is meant for **learning, OSINT practice, and authorized
security testing only** — for example, generating a candidate password
list for a system or account **you own or are explicitly authorized to
test**. Do not use it against systems you do not have permission to
test.
"""
    )
