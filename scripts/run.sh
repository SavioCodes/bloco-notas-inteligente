#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

if command -v python3 >/dev/null 2>&1; then
  python3 -m smart_notepad
elif command -v python >/dev/null 2>&1; then
  python -m smart_notepad
else
  echo "Python nao foi encontrado. Instale Python 3.10 ou superior."
  exit 1
fi
