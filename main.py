#!/usr/bin/env python3
"""One Line, One Laugh — writes a single funny line to /output/entry.txt.

Gate (competition.yaml): the entry file must be UTF-8 text of 1 to 140
characters, not only whitespace, one self-contained joke.
"""

import os

ENTRY = (
    "The dentist asked how my teeth were doing while both his hands "
    "were in my mouth, so I just nodded like a hostage."
)


def validate_entry(text: str) -> None:
    """Raise ValueError unless the entry satisfies the gate."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= 140):
        raise ValueError(
            f"entry must be 1-140 characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    # The entry is ONE line: no line breaks or carriage returns.
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line (no newline)")
    # The gate reads the file as UTF-8; fail loudly if it cannot encode.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"entry is not valid UTF-8 text: {exc}") from exc


def write_entry(text: str, out_dir: str) -> str:
    """Atomically write the entry to <out_dir>/entry.txt (mode 0644)."""
    validate_entry(text)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return target


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    write_entry(ENTRY, out_dir)


if __name__ == "__main__":
    main()
