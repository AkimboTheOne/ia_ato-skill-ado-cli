#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${REPO_ROOT}/.venv"

info() { echo "[INFO] $*"; }
warn() { echo "[WARN] $*"; }
err() { echo "[ERROR] $*" >&2; }

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

resolve_python() {
  local candidates=(
    python3.13
    python3.12
    python3.11
    python3
  )
  local candidate
  for candidate in "${candidates[@]}"; do
    if has_cmd "${candidate}" && "${candidate}" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
      echo "${candidate}"
      return 0
    fi
  done
  return 1
}

brew_hint() {
  local pkg="$1"
  if has_cmd brew; then
    echo "Try: brew install ${pkg}"
  else
    echo "Install '${pkg}' using your OS package manager."
  fi
}

if ! has_cmd make; then
  err "make is required but was not found."
  err "$(brew_hint make)"
  exit 1
fi

if ! PYTHON_BIN="$(resolve_python)"; then
  found_version="not-found"
  if has_cmd python3; then
    found_version="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  fi
  err "python>=3.11 is required. Found python3=${found_version}."
  err "$(brew_hint python)"
  exit 1
fi

PYTHON_VERSION="$("${PYTHON_BIN}" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
info "Using ${PYTHON_BIN} (version ${PYTHON_VERSION})"

if [ -d "${VENV_DIR}" ]; then
  info "Reusing virtual environment at ${VENV_DIR}"
else
  info "Creating virtual environment at ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

VENV_PYTHON="${VENV_DIR}/bin/python"
VENV_CLI="${VENV_DIR}/bin/ato-skill-ado-cli"

info "Upgrading pip in virtual environment"
"${VENV_PYTHON}" -m pip install --upgrade pip >/dev/null

info "Installing project in editable mode with dev dependencies"
"${VENV_PYTHON}" -m pip install -e ".[dev]"

if [ -x "${VENV_CLI}" ]; then
  info "Running post-install doctor check"
  "${VENV_CLI}" doctor --json || warn "Doctor reported warnings. Run '.venv/bin/ato-skill-ado-cli doctor --json' for details."
else
  warn "CLI executable not found at ${VENV_CLI}. You can run: ${VENV_PYTHON} -m ato_skill_ado_cli.main doctor --json"
fi

info "Install completed."
info "Use '. .venv/bin/activate' to activate the environment."
