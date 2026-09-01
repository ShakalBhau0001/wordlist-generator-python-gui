from __future__ import annotations

import itertools
import math
import os
import re
from dataclasses import dataclass, field
from datetime import datetime

# Leetspeak substitution map

LEET_MAP = str.maketrans(
    {
        "a": "4",
        "A": "4",
        "e": "3",
        "E": "3",
        "i": "1",
        "I": "1",
        "o": "0",
        "O": "0",
        "s": "5",
        "S": "5",
        "t": "7",
        "T": "7",
        "b": "8",
        "B": "8",
    }
)

SEPARATORS = ["", "-", "_", "."]

# Safety limits so bad input can't hang/crash the app
MAX_SAFE_BASE_PERMUTATIONS = 500_000
MAX_SAFE_BASE_WORDS = 300_000
MAX_SAFE_EXPANDED_WORDS = 5_000_000
MAX_SAFE_FINAL_WORDS = 8_000_000


def clean_token(s: str) -> str:
    """Keeping only alphanumerics + . _ -"""
    s = re.sub(r"\s+", "", s.strip())
    return re.sub(r"[^0-9A-Za-z._-]", "", s)


def case_variants(s: str) -> set[str]:
    if not s:
        return {s}
    variants = {s, s.lower(), s.upper(), s.capitalize()}
    parts = re.split(r"[_\-.]", s)
    camel = "".join(p.capitalize() for p in parts if p)
    if camel:
        variants.add(camel)
        variants.add(camel.lower())
    return variants


def leet_variants(s: str) -> set[str]:
    return {s, s.translate(LEET_MAP)}


def with_separators(tokens: tuple[str, ...], add_separators: bool) -> set[str]:
    if len(tokens) == 1:
        return {tokens[0]}
    seps = SEPARATORS if add_separators else [""]
    return {sep.join(tokens) for sep in seps}


def add_numeric_tails(words: set[str], tails: list[str]) -> set[str]:
    out = set(words)
    for w in words:
        for t in tails:
            out.add(f"{w}{t}")
    return out


def unique_len_filtered(words: set[str], min_len: int, max_len: int) -> set[str]:
    return {w for w in words if min_len <= len(w) <= max_len}


def parse_date_tokens(date_str: str) -> set[str]:
    """Parsing date into day/month/year sub-tokens."""
    tokens: set[str] = set()
    ds = re.sub(r"[^\d]", "", date_str)
    if len(ds) == 8:  # ddmmyyyy
        day, month, year = ds[:2], ds[2:4], ds[4:]
    elif len(ds) == 6:  # ddmmyy
        day, month, yy = ds[:2], ds[2:4], ds[4:]
        century = "20" if int(yy) <= 30 else "19"
        year = century + yy
    else:
        day = month = year = ""

    for piece in (day, month, year, ds):
        if piece:
            tokens.add(piece)
    if day and month and year:
        tokens.update(
            {day + month, month + day, day + month + year, year + month + day}
        )
    return tokens


def get_unique_filename(basename: str, ext: str, directory: str = ".") -> str:
    """Avoid overwriting an existing file."""
    candidate = os.path.join(directory, f"{basename}{ext}")
    if not os.path.exists(candidate):
        return candidate
    i = 1
    while os.path.exists(os.path.join(directory, f"{basename}-{i}{ext}")):
        i += 1
    return os.path.join(directory, f"{basename}-{i}{ext}")


def build_tokens(
    first: str = "",
    last: str = "",
    nick: str = "",
    team: str = "",
    date_str: str = "",
) -> list[str]:
    """Clean + de-duplicate all input fields into a token list."""
    tokens = [clean_token(x) for x in (first, last, nick, team) if x and x.strip()]
    if date_str and date_str.strip():
        tokens.extend(sorted(parse_date_tokens(date_str)))
    tokens = [t for t in tokens if t]
    return list(dict.fromkeys(tokens))


def estimate_permutation_count(tokens: list[str], max_combo: int) -> int:
    """Rough pre-check estimate before running full permutations."""
    n = len(tokens)
    max_combo = min(max_combo, n)
    total = 0
    for r in range(1, max_combo + 1):
        total += math.perm(n, r)
    return total


@dataclass
class WordlistConfig:
    min_len: int = 7
    max_len: int = 24
    max_combo: int = 3
    use_case_variants: bool = True
    use_leet: bool = True
    use_separators: bool = True
    use_numeric_tails: bool = True
    numeric_tail_years_back: int = 10

    def validate(self) -> list[str]:
        problems: list[str] = []
        if self.min_len < 1:
            problems.append("Minimum length must be at least 1.")
        if self.max_len < self.min_len:
            problems.append("Maximum length must be >= minimum length.")
        if self.max_combo < 1:
            problems.append("Max combo must be at least 1.")
        if self.max_combo > 6:
            problems.append("Max combo above 6 is not supported (too slow/large).")
        return problems


@dataclass
class GenerationResult:
    words: list[str] = field(default_factory=list)  # type: ignore
    tokens_used: list[str] = field(default_factory=list)  # type: ignore
    base_permutation_count: int = 0

    @property
    def count(self) -> int:
        return len(self.words)

    def as_text(self) -> str:
        return "\n".join(self.words) + ("\n" if self.words else "")


# Custom error for oversized configs
class WordlistTooLargeError(ValueError):
    """Raised when config would generate too large a wordlist."""


def build_wordlist(tokens: list[str], config: WordlistConfig) -> set[str]:
    """Build candidate word set with staged safety checks."""
    tokens = [t for t in tokens if t]
    tokens = list(dict.fromkeys(tokens))
    if not tokens:
        return set()

    max_combo = min(config.max_combo, len(tokens))

    # Stage 0: pre-check before permutations loop
    base_permutation_estimate = estimate_permutation_count(tokens, max_combo)
    if base_permutation_estimate > MAX_SAFE_BASE_PERMUTATIONS:
        raise WordlistTooLargeError(
            f"Estimated {base_permutation_estimate:,} base permutations - "
            "too large. Reduce 'Max tokens combined per word' or fields used."
        )

    base: set[str] = set()
    for r in range(1, max_combo + 1):
        for combo in itertools.permutations(tokens, r):
            base.update(with_separators(combo, config.use_separators))

    # Stage 1: check after permutations + separators
    if len(base) > MAX_SAFE_BASE_WORDS:
        raise WordlistTooLargeError(
            f"Base word set reached {len(base):,} entries - too large. "
            "Reduce 'Max tokens combined per word' or turn off separators."
        )

    expanded: set[str] = set()
    for w in base:
        variants = {w}
        if config.use_case_variants:
            variants = set().union(*(case_variants(x) for x in variants))  # type: ignore
        if config.use_leet:
            variants = set().union(*(leet_variants(x) for x in variants))  # type: ignore
        expanded.update(variants)

        # Stage 2: check during case/leet expansion loop
        if len(expanded) > MAX_SAFE_EXPANDED_WORDS:
            raise WordlistTooLargeError(
                f"Word set exceeded {MAX_SAFE_EXPANDED_WORDS:,} entries during "
                "case/leetspeak expansion. Turn off case variants or leetspeak."
            )

    if config.use_numeric_tails:
        try:
            now_year = datetime.now().year  # noqa: DTZ005
        except Exception:  # noqa: BLE001
            now_year = 2026
        tails = [str(i) for i in range(100)] + [
            str(y)
            for y in range(now_year - config.numeric_tail_years_back, now_year + 1)
        ]

        # Stage 3: check before numeric tail multiplication
        projected = len(expanded) * (len(tails) + 1)
        if projected > MAX_SAFE_FINAL_WORDS:
            raise WordlistTooLargeError(
                f"Numeric tails would produce ~{projected:,} entries - too large. "
                "Turn off numeric tail suffixes or reduce other options."
            )
        expanded = add_numeric_tails(expanded, tails)

    return unique_len_filtered(expanded, config.min_len, config.max_len)


def generate_wordlist(
    first: str = "",
    last: str = "",
    nick: str = "",
    team: str = "",
    date_str: str = "",
    config: WordlistConfig | None = None,
) -> GenerationResult:
    """Main entry point used by the GUI."""
    config = config or WordlistConfig()
    problems = config.validate()
    if problems:
        raise ValueError(" ".join(problems))

    tokens = build_tokens(first, last, nick, team, date_str)
    if not tokens:
        raise ValueError(
            "No input provided. Fill in at least one field "
            "(first name, last name, nickname, team, or date)."
        )

    base_count = estimate_permutation_count(tokens, config.max_combo)

    # build_wordlist raises WordlistTooLargeError if config is unsafe
    words = sorted(build_wordlist(tokens, config))
    return GenerationResult(
        words=words, tokens_used=tokens, base_permutation_count=base_count
    )
