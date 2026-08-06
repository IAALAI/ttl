#!/usr/bin/env bash
# Validate the ttl Victoria 3 mod.
#
# Always runs the offline well-formedness checks (scripts/validate_mod.py).
# If a Victoria 3 game directory is available (via the VIC3_DIR environment
# variable or a standard Steam path) and vic3-tiger is installed, it also runs
# the full vic3-tiger semantic validation.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== Offline well-formedness checks =="
python3 "$ROOT/scripts/validate_mod.py" "$ROOT"

if command -v vic3-tiger >/dev/null 2>&1; then
  GAME_DIR="${VIC3_DIR:-}"
  if [[ -z "$GAME_DIR" ]]; then
    for candidate in \
      "$HOME/.steam/steam/steamapps/common/Victoria 3" \
      "$HOME/.local/share/Steam/steamapps/common/Victoria 3"; do
      if [[ -d "$candidate" ]]; then
        GAME_DIR="$candidate"
        break
      fi
    done
  fi

  echo
  if [[ -n "$GAME_DIR" && -d "$GAME_DIR" ]]; then
    echo "== vic3-tiger full validation (game: $GAME_DIR) =="
    vic3-tiger --no-color --game "$GAME_DIR" "$ROOT"
  else
    echo "== vic3-tiger =="
    echo "vic3-tiger is installed ($(vic3-tiger --version))."
    echo "Set VIC3_DIR to your Victoria 3 install to run full semantic validation, e.g.:"
    echo "  VIC3_DIR=\"/path/to/Victoria 3\" $ROOT/scripts/validate.sh"
  fi
else
  echo
  echo "vic3-tiger not installed; skipping full semantic validation."
fi
