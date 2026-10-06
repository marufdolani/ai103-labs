# Runs after `azd up` / `azd provision` on Windows: writes .env, installs Python deps, checks the platform.
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

Write-Host '==> Writing .env from azd environment'
azd env get-values | Out-File -Encoding utf8 .env

if (-not (Test-Path .venv)) {
  Write-Host '==> Creating virtual environment (.venv)'
  python -m venv .venv
}
& .\.venv\Scripts\Activate.ps1
Write-Host '==> Installing Python requirements'
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

Write-Host '==> Generating starter files'
python -m labkit make-starters | Out-Null

Write-Host '==> Platform check'
try { python -m labkit doctor } catch { Write-Warning 'Re-run: python -m labkit doctor (RBAC can take a few minutes)' }
Write-Host "`nReady. Start with: python -m labkit open 01"
