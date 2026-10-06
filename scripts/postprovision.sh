#!/usr/bin/env sh
# Runs after `azd up` / `azd provision`: writes .env, installs Python deps, checks the platform.
set -e
cd "$(dirname "$0")/.."

echo "==> Writing .env from azd environment"
azd env get-values > .env

if [ ! -d .venv ]; then
  echo "==> Creating virtual environment (.venv)"
  python3 -m venv .venv
fi
. .venv/bin/activate
echo "==> Installing Python requirements"
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

echo "==> Generating starter files"
python -m labkit make-starters >/dev/null

echo "==> Platform check (RBAC can take a few minutes to propagate; re-run './lab doctor' if a check fails)"
python -m labkit doctor || true
echo
echo "Ready. Start with: ./lab open 01"
