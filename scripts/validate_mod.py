#!/usr/bin/env python3
"""Offline well-formedness validator for the `ttl` Victoria 3 mod.

This performs the checks that are possible *without* the copyrighted Victoria 3
game files (which cannot be shipped in CI or a Cloud Agent VM):

  * Paradox script (`.txt`) brace and quote balance.
  * Localization (`.yml`) format: UTF-8 BOM, `l_<language>:` header, entry syntax.
  * `.metadata/metadata.json` is valid JSON.
  * Image assets (`.png`) have a valid PNG signature.

For full semantic validation (missing localizations, scope checks, undefined
references, ...) run `vic3-tiger` with a real Victoria 3 install:

  vic3-tiger --game "/path/to/Victoria 3" .

Exit code is non-zero if any error is found, so this doubles as a CI/pre-commit
check.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Directories (relative to the mod root) that contain Paradox script files.
SCRIPT_DIRS = ["common", "events"]
LOC_DIR = "localization"
METADATA_FILE = ".metadata/metadata.json"

LOC_ENTRY_RE = re.compile(r'^\s+[A-Za-z0-9_.\-]+:\d*\s+".*"\s*$')
LOC_HEADER_RE = re.compile(r"^l_[a-z_]+:\s*$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checked = 0

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def strip_script_line(line: str) -> str:
    """Remove comments and quoted-string contents from a Paradox script line.

    Returns a version of the line safe for brace counting: everything inside a
    double-quoted string and everything after an unquoted `#` is removed.
    """
    out = []
    in_string = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_string:
            if ch == "\\":  # skip escaped char inside string
                i += 2
                continue
            if ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
        elif ch == "#":
            break
        else:
            out.append(ch)
        i += 1
    return "".join(out), in_string


def check_script_file(path: Path, rep: Report) -> None:
    rep.checked += 1
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        rep.error(f"{path}: not valid UTF-8 ({exc})")
        return

    depth = 0
    for lineno, raw in enumerate(text.splitlines(), start=1):
        cleaned, unterminated_string = strip_script_line(raw)
        if unterminated_string:
            rep.error(f"{path}:{lineno}: unterminated quoted string")
        for ch in cleaned:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    rep.error(
                        f"{path}:{lineno}: unbalanced '}}' "
                        f"(closing brace with no matching '{{')"
                    )
                    depth = 0
    if depth != 0:
        rep.error(f"{path}: {depth} unclosed '{{' brace(s) at end of file")


def check_loc_file(path: Path, rep: Report) -> None:
    rep.checked += 1
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        rep.error(
            f"{path}: missing UTF-8 BOM (Victoria 3 localization files must be "
            f"UTF-8 with BOM or the game silently ignores them)"
        )
    text = raw.decode("utf-8-sig")

    header_seen = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not header_seen:
            if not LOC_HEADER_RE.match(line):
                rep.error(
                    f"{path}:{lineno}: first entry must be a language header "
                    f"like 'l_english:' (found: {line.strip()!r})"
                )
            header_seen = True
            continue
        if line.count('"') % 2 != 0:
            rep.error(f"{path}:{lineno}: odd number of '\"' (unterminated value)")
            continue
        if not LOC_ENTRY_RE.match(line):
            rep.warn(
                f"{path}:{lineno}: entry does not match 'KEY:<n> \"value\"' "
                f"format ({line.strip()!r})"
            )
    if not header_seen:
        rep.error(f"{path}: no 'l_<language>:' header found")


def check_metadata(path: Path, rep: Report) -> None:
    if not path.exists():
        rep.warn(f"{path}: metadata file not found")
        return
    rep.checked += 1
    try:
        json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        rep.error(f"{path}: invalid JSON ({exc})")


def check_png(path: Path, rep: Report) -> None:
    rep.checked += 1
    sig = path.read_bytes()[:8]
    if sig != b"\x89PNG\r\n\x1a\n":
        rep.error(f"{path}: not a valid PNG (bad signature)")


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    if not root.exists():
        print(f"error: mod root {root} does not exist", file=sys.stderr)
        return 2

    rep = Report()

    for d in SCRIPT_DIRS:
        for p in sorted((root / d).rglob("*.txt")):
            check_script_file(p, rep)

    loc_root = root / LOC_DIR
    if loc_root.exists():
        for p in sorted(loc_root.rglob("*.yml")):
            check_loc_file(p, rep)

    check_metadata(root / METADATA_FILE, rep)

    for p in sorted(root.rglob("*.png")):
        if ".git" in p.parts:
            continue
        check_png(p, rep)

    print(f"Validated {rep.checked} file(s) under {root}")
    for w in rep.warnings:
        print(f"  WARN  {w}")
    for e in rep.errors:
        print(f"  ERROR {e}")

    if rep.errors:
        print(f"\nFAILED: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
        return 1
    print(f"\nOK: 0 errors, {len(rep.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
