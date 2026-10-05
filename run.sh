#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
probe='import sys; sys.exit(sys.version_info < (3, 10))'
if [[ -n ${PYTHON:-} ]]; then
    if "$PYTHON" -c "$probe" >/dev/null 2>&1; then
        exec "$PYTHON" -X utf8 "$root/src/main.py" "$@"
    fi
    printf 'PYTHON must point to a working Python 3.10+ executable.\n' >&2
    exit 1
fi
for candidate in python3 python; do
    if "$candidate" -c "$probe" >/dev/null 2>&1; then
        exec "$candidate" -X utf8 "$root/src/main.py" "$@"
    fi
done
printf 'Python 3.10+ is required. Set PYTHON to its executable.\n' >&2
exit 1
