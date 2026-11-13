#!/usr/bin/env bash
# ==============================================================================
# Agentic SDLC OS — Bootstrap Script for POSIX (Linux/macOS)
# Initializes environment, installs git hooks, validates framework integrity
# ==============================================================================
set -e

echo "================================================================================"
echo "         AGENTIC SDLC OS — AUTOMATED REPOSITORY BOOTSTRAP                       "
echo "================================================================================"

# 1. Check Git
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed or not in PATH."
    exit 1
fi
echo "[OK] Git detected: $(git --version)"

# 2. Check Python
PYTHON_BIN="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_BIN="python"
    else
        echo "[ERROR] Python is not installed. Python 3.10+ is required."
        exit 1
    fi
fi
echo "[OK] Python detected: $($PYTHON_BIN --version)"

# 3. Configure Git Pre-Commit Hook
if [ -d ".git/hooks" ]; then
    HOOK_PATH=".git/hooks/pre-commit"
    cat << 'EOF' > "$HOOK_PATH"
#!/bin/sh
echo "[PRE-COMMIT] Scanning for plaintext secrets and credentials..."
python3 scripts/security_check.py --stage audit 2>/dev/null || python scripts/security_check.py --stage audit
if [ $? -ne 0 ]; then
    echo "[PRE-COMMIT BLOCKED] Commit contains hardcoded secrets or security violations."
    exit 1
fi
EOF
    chmod +x "$HOOK_PATH"
    echo "[OK] Git pre-commit security hook installed at $HOOK_PATH"
fi

# 4. Initialize Traceability Ledger
echo "[INFO] Initializing Traceability Ledger..."
$PYTHON_BIN scripts/traceability_cli.py init

# 5. Run Framework Validation Suite
echo "[INFO] Running Framework Integrity Validation Suite..."
$PYTHON_BIN scripts/validate_framework.py

echo ""
echo "================================================================================"
echo "       [SUCCESS] AGENTIC SDLC OS BOOTSTRAP COMPLETE!                            "
echo "================================================================================"
echo ""
echo "Available Core Commands:"
echo "  - Create Task:        python scripts/traceability_cli.py create-task --domain <domain> --title '<title>'"
echo "  - Validate Gate:      python scripts/gate_validator.py --gate <G0..G11> --task <TASK_ID>"
echo "  - Security Audit:     python scripts/security_check.py --stage audit"
echo "  - Ledger Status:      python scripts/traceability_cli.py status"
echo "  - Traceability Matrix:python scripts/traceability_cli.py matrix"
echo ""
echo "Next Step: Start your workflow in Antigravity using 'sdlc-orchestrator' or run a skill."
