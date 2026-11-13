# ==============================================================================
# Agentic SDLC OS — Bootstrap Script for Windows PowerShell
# Initializes environment, installs git hooks, validates framework integrity
# ==============================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "         AGENTIC SDLC OS — AUTOMATED REPOSITORY BOOTSTRAP                       " -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 1. Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed or not in PATH. Please install Git first."
    exit 1
}
Write-Host "[OK] Git detected." -ForegroundColor Green

# 2. Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH. Python 3.10+ is required."
    exit 1
}
$pyVer = python --version
Write-Host "[OK] Python detected: $pyVer" -ForegroundColor Green

# 3. Configure Git Pre-Commit Hook (Optional on Windows)
$shPath = "C:\Program Files\Git\usr\bin\sh.exe"
$hookDir = ".git/hooks"
if ((Test-Path $shPath) -and (Test-Path $hookDir)) {
    $preCommitPath = Join-Path $hookDir "pre-commit"
    $hookContent = @"
#!/bin/sh
# Agentic SDLC OS Pre-Commit Security Hook
python scripts/security_check.py --stage audit 2>/dev/null || python3 scripts/security_check.py --stage audit
"@
    Set-Content -Path $preCommitPath -Value $hookContent -Encoding UTF8
    Write-Host "[OK] Git pre-commit security hook installed at $preCommitPath" -ForegroundColor Green
} else {
    Write-Host "[INFO] Git pre-commit hook skipped on Windows (use 'python scripts/security_check.py --stage audit' for audits)." -ForegroundColor Yellow
}

# 4. Initialize Traceability Ledger
Write-Host "[INFO] Initializing Traceability Ledger..." -ForegroundColor Yellow
python scripts/traceability_cli.py init

# 5. Run Framework Validation Suite
Write-Host "[INFO] Running Framework Integrity Validation Suite..." -ForegroundColor Yellow
python scripts/validate_framework.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Framework integrity validation failed."
    exit 1
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "       [SUCCESS] AGENTIC SDLC OS BOOTSTRAP COMPLETE!                            " -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Available Core Commands:" -ForegroundColor Yellow
Write-Host "  - Create Task:        python scripts/traceability_cli.py create-task --domain <domain> --title '<title>'"
Write-Host "  - Validate Gate:      python scripts/gate_validator.py --gate <G0..G11> --task <TASK_ID>"
Write-Host "  - Security Audit:     python scripts/security_check.py --stage audit"
Write-Host "  - Ledger Status:      python scripts/traceability_cli.py status"
Write-Host "  - Traceability Matrix:python scripts/traceability_cli.py matrix"
Write-Host ""
Write-Host "Next Step: Start your workflow in Antigravity using 'sdlc-orchestrator' or run a skill."
