#!/usr/bin/env bash
#
# run.sh — set up dependencies, then run the NC Housing model.
# ---------------------------------------------------------------------------
# Any arguments you pass are forwarded straight to the Python script, so:
#
#   ./run.sh                          # full run, timestamped PNGs + log
#   ./run.sh --quick                  # fast smoke test
#   ./run.sh --data path/to.csv       # point at a specific CSV
#   ./run.sh --show                   # open plot windows instead of saving
#
# By default this creates a local virtual environment (.venv) so installs
# don't collide with the system Python (and to sidestep the "externally
# managed environment" pip error on newer images). To install into the
# current environment instead, run:  USE_VENV=0 ./run.sh
# ---------------------------------------------------------------------------

# Fail loudly: stop on the first error, on unset variables, and on any
# failure inside a pipeline.
set -euo pipefail

# Always operate from the folder this script lives in, no matter where it's
# called from.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

SCRIPT="nc_housing_model_v2.py"
REQS="requirements.txt"
USE_VENV="${USE_VENV:-1}"   # 1 = use a venv (default), 0 = use current env

# 1. (Optional) create + activate an isolated virtual environment.
if [ "$USE_VENV" = "1" ]; then
  if [ ! -d ".venv" ]; then
    echo ">> Creating virtual environment in .venv ..."
    python3 -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  echo ">> Using Python: $(which python)"
fi

# 2. Install dependencies. pip is idempotent — already-satisfied packages are
#    skipped, so re-running this is cheap after the first time.
echo ">> Installing dependencies from $REQS ..."
python -m pip install --upgrade pip
python -m pip install -r "$REQS"

# 3. Run the model, passing along whatever CLI args were given to run.sh.
echo ">> Running $SCRIPT ..."
python "$SCRIPT" "$@"
