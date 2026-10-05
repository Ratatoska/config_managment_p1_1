#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")/.." && pwd -P)
cd -- "$root"
if [[ -n ${PYTHON:-} ]]; then
    python_command=("$PYTHON")
elif python3 -c "import sys" >/dev/null 2>&1; then
    python_command=(python3)
else
    python_command=(python)
fi
"${python_command[@]}" -X utf8 scripts/check_quality.py
"${python_command[@]}" -X utf8 -m unittest discover -s tests -v
for script in run.sh scripts/*.sh; do
    bash -n "$script"
done
if command -v shellcheck >/dev/null 2>&1; then
    shellcheck run.sh scripts/*.sh
fi
