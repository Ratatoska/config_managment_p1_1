#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")/.." && pwd -P)
cd -- "$root"
bash run.sh examples/vfs.json --headless < /dev/null
