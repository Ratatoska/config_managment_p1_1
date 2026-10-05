#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")/.." && pwd -P)
cd -- "$root"
bash run.sh examples/vfs.json examples/startup_stage2.txt --headless
