from __future__ import annotations

import streamlit as st

import core.engine
from core import (
    GenerationResult,
    WordlistConfig,
    estimate_permutation_count,
    generate_wordlist,
)

RESULT_KEY = "wordlist_result"


def _sidebar_options() -> WordlistConfig:
    """Render the generation-options controls and return a WordlistConfig."""
    st.markdown("#### ⚙️ Generation options")
    len_col1, len_col2 = st.columns(2)
    with len_col1:
        min_len = st.number_input(
            "Minimum length", min_value=1, max_value=64, value=7, step=1
        )
    with len_col2:
        max_len = st.number_input(
            "Maximum length", min_value=1, max_value=64, value=24, step=1
        )

    max_combo = st.slider(
        "Max tokens combined per word",
        min_value=1,
        max_value=6,
        value=3,
        help=(
            "How many input fields get combined together in one word "
            "(e.g. 2 = firstlast, lastfirst, ...). Higher values grow "
            "very fast -- keep it at 2-3 for most cases."
        ),
    )

    opt_col1, opt_col2 = st.columns(2)
    with opt_col1:
        use_case = st.checkbox("Case variants (lower / UPPER / Camel)", value=True)
        use_separators = st.checkbox("Separators ( - _ . )", value=True)
    with opt_col2:
        use_leet = st.checkbox("Leetspeak (a→4, e→3, ...)", value=True)
        use_numbers = st.checkbox("Numeric tail suffixes (00-99, years)", value=True)

    return WordlistConfig(
        min_len=int(min_len),
        max_len=int(max_len),
        max_combo=int(max_combo),
        use_case_variants=use_case,
        use_leet=use_leet,
        use_separators=use_separators,
        use_numeric_tails=use_numbers,
    )


def render() -> None:
    st.markdown("## Wordlist Generator")
    st.caption(
        "Build a targeted, personal-info-based password wordlist for "
        "authorized security testing, OSINT practice, and learning."
    )

    with st.form("wordlist_form"):
        st.markdown("#### 🧑 Personal info")
        c1, c2 = st.columns(2)
        with c1:
            first = st.text_input("First name", placeholder="John")
            nick = st.text_input("Nickname (optional)", placeholder="JD")
        with c2:
            last = st.text_input("Last name", placeholder="Doe")
            team = st.text_input("Team / Company (optional)", placeholder="RedTeam")

        date_str = st.text_input(
            "Date (optional)",
            placeholder="dd/mm/yyyy or ddmmyyyy, e.g. 15/08/1995",
            help="Accepts dd/mm/yyyy, ddmmyyyy, or ddmmyy.",
        )

        st.markdown("---")
        config = _sidebar_options()

        st.markdown("---")
        output_name = st.text_input(
            "Output file name (without extension)", value="wordlist"
        )

        submitted = st.form_submit_button(
            "🚀 Generate wordlist", use_container_width=True
        )

    if submitted:
        config_problems = config.validate()
        if config_problems:
            st.error(" ".join(config_problems))
            return

        tokens_preview = core.engine.build_tokens(first, last, nick, team, date_str)
        if tokens_preview:
            estimate = estimate_permutation_count(tokens_preview, config.max_combo)
            if estimate > 200_000:
                st.warning(
                    f"Heads up: this configuration will build roughly "
                    f"**{estimate:,}** base permutations before variant "
                    "expansion. This may take a little while."
                )

        try:
            with st.spinner("Generating wordlist....."):
                result = generate_wordlist(
                    first=first,
                    last=last,
                    nick=nick,
                    team=team,
                    date_str=date_str,
                    config=config,
                )
        except ValueError as exc:
            st.error(str(exc))
            st.session_state.pop(RESULT_KEY, None)
            return

        st.session_state[RESULT_KEY] = result
        st.session_state["wordlist_output_name"] = output_name.strip() or "wordlist"

    result: GenerationResult | None = st.session_state.get(RESULT_KEY)
    if result is not None:
        _render_results(
            result, st.session_state.get("wordlist_output_name", "wordlist")
        )


def _render_results(result: GenerationResult, output_name: str) -> None:
    st.markdown("---")
    st.markdown("#### ✅ Results")
    m1, m2, m3 = st.columns(3)
    m1.metric("Words generated", f"{result.count:,}")
    m2.metric("Tokens used", str(len(result.tokens_used)))
    m3.metric("Base permutations", f"{result.base_permutation_count:,}")
    with st.expander("Tokens used"):
        st.write(", ".join(result.tokens_used) if result.tokens_used else "—")

    with st.expander(f"Preview (first {min(50, result.count)} words)", expanded=True):
        preview = result.words[:50]
        if preview:
            st.dataframe({"word": preview}, use_container_width=True, hide_index=True)
        else:
            st.info("No words matched the current length filters.")

    file_bytes = result.as_text().encode("utf-8")
    st.download_button(
        label=f"⬇️ Download {output_name}.txt",
        data=file_bytes,
        file_name=f"{output_name}.txt",
        mime="text/plain",
        use_container_width=True,
    )
