#!/usr/bin/env bash
set -euo pipefail
cp -n .env.example .env || true
cp -n config.example.yaml config.yaml || true
