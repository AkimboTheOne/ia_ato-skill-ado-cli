#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_BIN_DIR="${ROOT_DIR}/.venv/bin"
CLI_BIN="${VENV_BIN_DIR}/ato-skill-ado-cli"

RUN_CONFIG_INIT=1
RUN_TESTS=0

usage() {
  cat <<'EOF'
Usage: ./scripts/setup.sh [options]

Options:
  --skip-config-init   Skip 'ato-skill-ado-cli config init'
  --with-tests         Run '.venv/bin/pytest -q' at the end
  -h, --help           Show this help
EOF
}

for arg in "$@"; do
  case "${arg}" in
    --skip-config-init) RUN_CONFIG_INIT=0 ;;
    --with-tests) RUN_TESTS=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown option: ${arg}" >&2
      usage
      exit 2
      ;;
  esac
done

echo "[STEP] Install dependencies in local .venv"
"${ROOT_DIR}/scripts/install.sh"

echo "[STEP] Bootstrap local config files"
make -C "${ROOT_DIR}" bootstrap

if [ "${RUN_CONFIG_INIT}" -eq 1 ]; then
  if [ -x "${CLI_BIN}" ]; then
    echo "[STEP] Initialize config.yaml via CLI"
    "${CLI_BIN}" config init
  else
    echo "[WARN] CLI not found at ${CLI_BIN}; skipping 'config init'"
  fi
fi

echo "[STEP] Run setup assistant checks"
"${ROOT_DIR}/scripts/doctor.sh"

if [ "${RUN_TESTS}" -eq 1 ]; then
  if [ -x "${VENV_BIN_DIR}/pytest" ]; then
    echo "[STEP] Run test suite"
    "${VENV_BIN_DIR}/pytest" -q
  else
    echo "[WARN] pytest not found in .venv; skipping tests"
  fi
fi

echo "[DONE] Setup completed successfully."
