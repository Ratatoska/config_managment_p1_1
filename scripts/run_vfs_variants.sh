#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")/.." && pwd -P)
cd -- "$root"
for vfs in vfs_minimal.json vfs_files.json vfs.json; do
    bash run.sh "examples/$vfs" examples/startup_stage3.txt --headless
done
if bash run.sh examples/missing.json --headless < /dev/null; then
    printf 'Expected missing-file error\n' >&2
    exit 1
fi
if bash run.sh examples/vfs_invalid.json --headless < /dev/null; then
    printf 'Expected invalid-format error\n' >&2
    exit 1
fi
