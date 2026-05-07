#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_CLI="${ROOT_DIR}/.venv/bin/ato-skill-ado-cli"

status_ok=0
status_warn=0
status_fail=0

ok() {
  echo "[OK] $*"
  status_ok=$((status_ok + 1))
}

warn() {
  echo "[WARN] $*"
  status_warn=$((status_warn + 1))
}

fail() {
  echo "[FAIL] $*" >&2
  status_fail=$((status_fail + 1))
}

if [ -d "${ROOT_DIR}/.venv" ]; then
  ok "Virtual environment found at .venv"
else
  fail "Virtual environment not found (.venv). Run 'make install'."
fi

if command -v jq >/dev/null 2>&1; then
  ok "Optional dependency 'jq' is available"
else
  warn "Optional dependency 'jq' not found (recommended for JSON workflows)"
fi

if [ -f "${ROOT_DIR}/.env" ]; then
  ok ".env found"
else
  warn ".env not found. Run 'make bootstrap' and fill Azure DevOps credentials."
fi

if [ -f "${ROOT_DIR}/config.yaml" ]; then
  ok "config.yaml found"
else
  warn "config.yaml not found. Run 'make bootstrap' and adjust settings."
fi

if [ -x "${VENV_CLI}" ]; then
  if "${VENV_CLI}" doctor --json >/dev/null; then
    ok "CLI doctor passed using .venv"
  else
    fail "CLI doctor reported a failure (run '.venv/bin/ato-skill-ado-cli doctor --json')."
  fi
elif command -v ato-skill-ado-cli >/dev/null 2>&1; then
  if ato-skill-ado-cli doctor --json >/dev/null; then
    ok "CLI doctor passed using PATH executable"
  else
    fail "CLI doctor reported a failure (run 'ato-skill-ado-cli doctor --json')."
  fi
else
  fail "ato-skill-ado-cli executable not found. Run 'make install'."
fi

echo ""
echo "Summary: OK=${status_ok} WARN=${status_warn} FAIL=${status_fail}"
if [ "${status_fail}" -gt 0 ]; then
  exit 1
fi
