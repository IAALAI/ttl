#!/usr/bin/env bash
# Idempotent environment bootstrap for the ttl Victoria 3 mod.
#
# Installs `vic3-tiger` (the canonical Victoria 3 mod validator) and makes the
# repository's validation scripts executable. Safe to run repeatedly.
set -euo pipefail

TIGER_VERSION="v1.19.0"
INSTALL_DIR="/usr/local/bin"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Prefer sudo when we are not root and it is available.
SUDO=""
if [[ "$(id -u)" -ne 0 ]]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    INSTALL_DIR="$HOME/.local/bin"
  fi
fi
mkdir -p "$HOME/.local/bin"

install_vic3_tiger() {
  if command -v vic3-tiger >/dev/null 2>&1 && \
     vic3-tiger --version 2>/dev/null | grep -q "${TIGER_VERSION#v}"; then
    echo "vic3-tiger ${TIGER_VERSION} already installed."
    return
  fi

  local url tmp
  url="https://github.com/amtep/tiger/releases/download/${TIGER_VERSION}/vic3-tiger-linux-${TIGER_VERSION}.tar.gz"
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' RETURN

  echo "Downloading vic3-tiger ${TIGER_VERSION}..."
  local attempt delay=4
  for attempt in 1 2 3 4 5; do
    if curl -fsSL "$url" -o "$tmp/vic3-tiger.tar.gz"; then
      break
    fi
    if [[ "$attempt" -eq 5 ]]; then
      echo "ERROR: failed to download vic3-tiger after 5 attempts." >&2
      return 1
    fi
    echo "download failed (attempt $attempt), retrying in ${delay}s..."
    sleep "$delay"
    delay=$((delay * 2))
  done

  tar -xzf "$tmp/vic3-tiger.tar.gz" -C "$tmp"
  local bin
  bin="$(find "$tmp" -name vic3-tiger -type f | head -n1)"
  chmod +x "$bin"
  $SUDO install -m 0755 "$bin" "$INSTALL_DIR/vic3-tiger"
  echo "Installed vic3-tiger to $INSTALL_DIR/vic3-tiger"
}

install_vic3_tiger

chmod +x "$ROOT/scripts/validate.sh" "$ROOT/scripts/validate_mod.py"

echo
echo "Environment ready."
vic3-tiger --version || "$INSTALL_DIR/vic3-tiger" --version
python3 --version
