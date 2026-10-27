#!/usr/bin/env bash
set -euo pipefail
if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then python -m pip install -e .; fi
python -m compileall -q .
echo "Environment and syntax checks completed. Add the project-specific run command here."
