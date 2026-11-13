#!/usr/bin/env bash
# ==============================================================================
# Agentic SDLC OS — Universal Installer for Linux / macOS
# ==============================================================================
set -e

REPO_URL="https://github.com/hetpatel-dev/agentic-sdlc-os.git"
GLOBAL_MODE=false
SUBMODULE_MODE=false
TARGET_DIR="."

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --global|-g) GLOBAL_MODE=true ;;
        --submodule|-s) SUBMODULE_MODE=true ;;
        --target|-t) TARGET_DIR="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo "================================================================================"
echo "         AGENTIC SDLC OS — UNIVERSAL PROJECT INSTALLER                          "
echo "================================================================================"

if [ "$GLOBAL_MODE" = true ]; then
    PLUGIN_DIR="$HOME/.gemini/config/plugins/agentic-sdlc-os"
    echo "[INSTALL] Installing globally to $PLUGIN_DIR..."
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    LOCAL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

    if [ -f "$LOCAL_ROOT/plugin.json" ]; then
        echo "[LOCAL] Copying directly from local repository at '$LOCAL_ROOT'..."
        mkdir -p "$PLUGIN_DIR"
        cp -r "$LOCAL_ROOT"/* "$PLUGIN_DIR/"
    elif [ -d "$PLUGIN_DIR" ]; then
        echo "[UPDATE] Existing installation found. Pulling latest..."
        git -C "$PLUGIN_DIR" pull origin main
    else
        mkdir -p "$(dirname "$PLUGIN_DIR")"
        git clone "$REPO_URL" "$PLUGIN_DIR"
    fi
    echo "[OK] Global installation complete! Active across all workspaces."
    echo "     Verify with: agy plugin list"
    exit 0
fi

echo "[INSTALL] Installing Agentic SDLC OS into project at '$TARGET_DIR'..."

if [ "$SUBMODULE_MODE" = true ]; then
    echo "[GIT] Adding submodule at '.agents/sdlc-os'..."
    git submodule add "$REPO_URL" .agents/sdlc-os
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    LOCAL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

    IS_TEMP=false
    if [ -f "$LOCAL_ROOT/plugin.json" ]; then
        echo "[LOCAL] Deploying directly from local repository at '$LOCAL_ROOT'..."
        TEMP_SOURCE="$LOCAL_ROOT"
    else
        TEMP_DIR=$(mktemp -d)
        echo "[DOWNLOAD] Cloning latest release..."
        git clone --depth 1 "$REPO_URL" "$TEMP_DIR"
        TEMP_SOURCE="$TEMP_DIR"
        IS_TEMP=true
    fi

    mkdir -p "$TARGET_DIR"

    echo "[DEPLOY] Copying .agents, scripts, skills, agents, rules to '$TARGET_DIR'..."
    cp -r "$TEMP_SOURCE/.agents" "$TARGET_DIR/.agents"
    cp -r "$TEMP_SOURCE/scripts" "$TARGET_DIR/scripts"
    if [ -d "$TEMP_SOURCE/skills" ]; then
        cp -r "$TEMP_SOURCE/skills" "$TARGET_DIR/skills"
    fi
    if [ -d "$TEMP_SOURCE/agents" ]; then
        cp -r "$TEMP_SOURCE/agents" "$TARGET_DIR/agents"
    fi
    if [ -d "$TEMP_SOURCE/rules" ]; then
        cp -r "$TEMP_SOURCE/rules" "$TARGET_DIR/rules"
    fi

    # Governance: Deploy schemas & quality gates; ensure clean empty traceability ledger for new projects
    mkdir -p "$TARGET_DIR/governance/schemas"
    cp -r "$TEMP_SOURCE/governance/schemas/"* "$TARGET_DIR/governance/schemas/"
    cp "$TEMP_SOURCE/governance/quality_gates.json" "$TARGET_DIR/governance/"

    if [ ! -f "$TARGET_DIR/governance/traceability_ledger.json" ]; then
        cat << 'EOF' > "$TARGET_DIR/governance/traceability_ledger.json"
{
  "version": "1.0.0",
  "system": "Agentic SDLC OS",
  "last_updated": "2026-11-13T00:00:00Z",
  "objectives": {},
  "requirements": {},
  "adrs": {},
  "tasks": {}
}
EOF
    fi

    # Docs: Create empty directory structure and deploy templates ONLY (never scaffold testing/sample artifacts)
    for d in adr api architecture database governance operations product releases requirements security testing testing/performance templates; do
        mkdir -p "$TARGET_DIR/docs/$d"
    done
    cp -r "$TEMP_SOURCE/docs/templates/"* "$TARGET_DIR/docs/templates/"

    if [ ! -f "$TARGET_DIR/AGENTS.md" ]; then
        cp "$TEMP_SOURCE/AGENTS.md" "$TARGET_DIR/"
    fi
    if [ ! -f "$TARGET_DIR/GEMINI.md" ]; then
        cp "$TEMP_SOURCE/GEMINI.md" "$TARGET_DIR/"
    fi
    if [ ! -f "$TARGET_DIR/.gitignore" ]; then
        cp "$TEMP_SOURCE/.gitignore" "$TARGET_DIR/"
    fi

    if [ "$IS_TEMP" = true ]; then
        rm -rf "$TEMP_DIR"
    fi
fi

echo ""
echo "================================================================================"
echo "       [SUCCESS] AGENTIC SDLC OS INSTALLED INTO YOUR PROJECT!                  "
echo "================================================================================"
echo "Next Steps:"
echo "1. Run bootstrap:"
echo "   bash scripts/bootstrap.sh"
echo "2. Start delegating to 'sdlc-orchestrator' or invoke any of the 18 SDLC skills."
