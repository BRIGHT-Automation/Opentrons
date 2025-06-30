#!/usr/bin/env bash
set -euo pipefail

# 1. Move every .py from */src/ up to here
find . -mindepth 3 -maxdepth 3 -type f -name '*.py' -path './*/src/*.py' -exec mv -n "{}" . \;

# 2. Remove all subfolders
find . -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;

echo "Done: all .py files are in $(pwd), subfolders removed."
