#!/usr/bin/env python3
"""
update.py - Enterprise Safe Updater for Agentic SDLC OS
Safely upgrades framework core, rules, agents, skills, and tooling in downstream projects
while strictly preserving project source code, tests, documentation, and task ledgers.
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_REPO_URL = "https://github.com/hetpatel-dev/agentic-sdlc-os.git"

FRAMEWORK_MANIFESTS = [
    ".agents/rules.json",
    ".agents/skills.json",
    ".agents/agents.json",
    ".agents/hooks.json",
    ".agents/mcp_config.json",
    "governance/quality_gates.json"
]

PROTECTED_DIRS = [
    "src",
    "tests",
    "docs/adr",
    "docs/api",
    "docs/architecture",
    "docs/database",
    "docs/governance",
    "docs/operations",
    "docs/product",
    "docs/releases",
    "docs/requirements",
    "docs/security",
    "docs/testing",
    ".agents/agents/custom",
    ".agents/rules/custom",
    ".agents/skills/custom"
]

def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def backup_file_or_dir(src_path, backup_root, target_root):
    if not src_path.exists():
        return
    rel = src_path.relative_to(target_root)
    dest = backup_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src_path.is_dir():
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src_path, dest, ignore=shutil.ignore_patterns(".backup", "*.bak*", "__pycache__"))
    else:
        shutil.copy2(src_path, dest)

def copy_framework_tree(src_dir, dest_dir, preserve_custom=True):
    if not src_dir.exists():
        return []
    copied = []
    dest_dir.mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(src_dir):
        rel_root = Path(root).relative_to(src_dir)
        target_sub = dest_dir / rel_root
        
        # Preserve user custom directories
        if preserve_custom and "custom" in rel_root.parts:
            continue
        if ".backup" in rel_root.parts:
            continue

        target_sub.mkdir(parents=True, exist_ok=True)
        for f in files:
            src_file = Path(root) / f
            dest_file = target_sub / f
            shutil.copy2(src_file, dest_file)
            copied.append(str(dest_file))
    return copied

def migrate_ledger(ledger_path, target_version="1.0.1"):
    if not ledger_path.exists():
        return False, "Ledger does not exist"
    ledger = load_json(ledger_path)
    changed = False

    for key in ["objectives", "requirements", "adrs", "tasks"]:
        if key not in ledger or not isinstance(ledger[key], dict):
            ledger[key] = {}
            changed = True

    for tid, t in ledger.get("tasks", {}).items():
        if "traceability" not in t or not isinstance(t["traceability"], dict):
            t["traceability"] = {}
            changed = True
        trace = t["traceability"]
        for field, default_val in [
            ("objective_id", ""),
            ("requirement_ids", []),
            ("user_story_ids", []),
            ("adr_ids", []),
            ("commits", []),
            ("test_case_ids", []),
            ("release_version", "")
        ]:
            if field not in trace:
                trace[field] = default_val
                changed = True
        for list_field in ["artifacts", "gate_history", "risks"]:
            if list_field not in t:
                t[list_field] = []
                changed = True

    old_ver = ledger.get("version", "1.0.0")
    if old_ver != target_version:
        ledger["version"] = target_version
        changed = True

    if changed:
        save_json(ledger_path, ledger)
        return True, f"Migrated ledger from v{old_ver} to v{target_version}"
    return False, f"Ledger already at schema v{target_version}"

def rollback(backup_dir, target_root):
    bpath = Path(backup_dir)
    if not bpath.exists() or not bpath.is_dir():
        print(f"[ERROR] Backup directory not found: {backup_dir}", file=sys.stderr)
        return False
    print(f"[ROLLBACK] Restoring framework assets from {bpath} into {target_root}...")
    for root, dirs, files in os.walk(bpath):
        rel = Path(root).relative_to(bpath)
        dest_sub = target_root / rel
        dest_sub.mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy2(Path(root) / f, dest_sub / f)
    print("[SUCCESS] Rollback complete. Target restored to backup snapshot state.")
    return True

def run_update(source_path, target_root, dry_run=False, skip_validation=False):
    print("================================================================================")
    print("            AGENTIC SDLC OS — ENTERPRISE SAFE FRAMEWORK UPDATER                 ")
    print("================================================================================")
    print(f"Target Project: {target_root.resolve()}")
    print(f"Update Source:  {source_path.resolve()}")
    if dry_run:
        print("[MODE] DRY-RUN ONLY — No files will be modified.")

    # 1. Verify Target
    if not (target_root / ".agents").exists() and not (target_root / "governance").exists():
        print(f"[ERROR] Target directory '{target_root}' is not an Agentic SDLC OS project.", file=sys.stderr)
        return 1

    # Detect current version
    current_ver = "unknown"
    plugin_path = target_root / "plugin.json"
    if plugin_path.exists():
        current_ver = load_json(plugin_path).get("version", current_ver)
    elif (target_root / "governance/traceability_ledger.json").exists():
        current_ver = load_json(target_root / "governance/traceability_ledger.json").get("version", current_ver)

    # Detect source version
    source_ver = "latest"
    src_plugin = source_path / "plugin.json"
    if src_plugin.exists():
        source_ver = load_json(src_plugin).get("version", source_ver)

    print(f"Current Target Version: {current_ver}")
    print(f"Upstream Framework Version: {source_ver}")

    if dry_run:
        print("\n[PLAN] The following framework components would be upgraded:")
        print("  - Core agents:         .agents/agents/ (preserving .agents/agents/custom/)")
        print("  - Core rules:          .agents/rules/  (preserving .agents/rules/custom/)")
        print("  - Core skills:         .agents/skills/ (preserving .agents/skills/custom/)")
        print("  - Framework manifests: .agents/*.json")
        print("  - Automation scripts:  scripts/")
        print("  - Gate schemas:        governance/schemas/")
        print("  - Quality gate defs:   governance/quality_gates.json")
        print("  - Standard templates:  docs/templates/")
        print("  - Traceability schema: governance/traceability_ledger.json (in-place migration)")
        print("\n[PROTECTED] The following project components are guaranteed untouched:")
        for p in PROTECTED_DIRS:
            print(f"  - {p}/")
        print("  - All existing project tasks, requirements, objectives, and ADRs")
        return 0

    # 2. Create Pre-Update Backup Snapshot
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = target_root / ".agents" / ".backup" / f"pre-update-{current_ver}-{timestamp}"
    print(f"\n[BACKUP] Creating pre-update snapshot at {backup_root}...")
    backup_root.mkdir(parents=True, exist_ok=True)

    items_to_backup = [
        target_root / ".agents",
        target_root / "scripts",
        target_root / "governance/schemas",
        target_root / "governance/quality_gates.json",
        target_root / "governance/traceability_ledger.json",
        target_root / "docs/templates"
    ]
    for item in items_to_backup:
        backup_file_or_dir(item, backup_root, target_root)
    print(f"[OK] Pre-update snapshot secured.")

    # 3. Synchronize Framework Core
    print("\n[UPDATE] Synchronizing framework core assets...")
    
    # .agents (agents, rules, skills, manifests)
    copy_framework_tree(source_path / ".agents", target_root / ".agents", preserve_custom=True)

    # root agents, rules, skills mirrors if present in target
    if (target_root / "agents").exists():
        copy_framework_tree(source_path / "agents", target_root / "agents", preserve_custom=True)
    if (target_root / "rules").exists():
        copy_framework_tree(source_path / "rules", target_root / "rules", preserve_custom=True)
    if (target_root / "skills").exists():
        copy_framework_tree(source_path / "skills", target_root / "skills", preserve_custom=True)

    # scripts
    copy_framework_tree(source_path / "scripts", target_root / "scripts", preserve_custom=False)

    # governance (schemas and quality gates ONLY - NEVER overwrite ledger)
    gov_target = target_root / "governance"
    gov_target.mkdir(parents=True, exist_ok=True)
    copy_framework_tree(source_path / "governance/schemas", gov_target / "schemas", preserve_custom=False)
    shutil.copy2(source_path / "governance/quality_gates.json", gov_target / "quality_gates.json")

    # docs/templates ONLY (never touch project docs)
    templates_target = target_root / "docs/templates"
    templates_target.mkdir(parents=True, exist_ok=True)
    for tf in (source_path / "docs/templates").glob("*.md"):
        shutil.copy2(tf, templates_target / tf.name)

    # plugin.json if present
    if (source_path / "plugin.json").exists():
        shutil.copy2(source_path / "plugin.json", target_root / "plugin.json")

    print("[OK] Framework core files synchronized successfully.")

    # 4. Migrate Traceability Ledger in-place
    print("\n[MIGRATE] Verifying and migrating traceability ledger schema...")
    ledger_path = target_root / "governance/traceability_ledger.json"
    if ledger_path.exists():
        migrated, msg = migrate_ledger(ledger_path, target_version=source_ver)
        print(f"[LEDGER] {msg}")
    else:
        print("[LEDGER] No existing ledger found; initializing clean ledger.")
        clean = {
            "version": source_ver,
            "system": "Agentic SDLC OS",
            "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "objectives": {},
            "requirements": {},
            "adrs": {},
            "tasks": {}
        }
        save_json(ledger_path, clean)

    # 5. Post-Update Validation
    if not skip_validation:
        print("\n[VALIDATE] Running framework integrity validation suite...")
        val_script = target_root / "scripts/validate_framework.py"
        if val_script.exists():
            res = subprocess.run([sys.executable, str(val_script)], cwd=str(target_root))
            if res.returncode != 0:
                print(f"[WARNING] Validation tests reported errors! You can rollback using:", file=sys.stderr)
                print(f"          python scripts/update.py --rollback \"{backup_root}\"", file=sys.stderr)
                return res.returncode

        check_script = target_root / "scripts/traceability_cli.py"
        if check_script.exists():
            subprocess.run([sys.executable, str(check_script), "check"], cwd=str(target_root))

    print("\n" + "=" * 80)
    print(f"       [SUCCESS] UPGRADED AGENTIC SDLC OS TO v{source_ver}!                     ")
    print("=" * 80)
    print("Summary:")
    print(f"  - Framework Version:   v{current_ver} -> v{source_ver}")
    print(f"  - Protected Dirs:      src/, tests/, docs/*, custom extensions (UNTOUCHED)")
    print(f"  - Ledger State:        Preserved & upgraded in-place")
    print(f"  - Pre-Update Snapshot: {backup_root}")
    print("  - Rollback Command:    python scripts/update.py --rollback " + f'"{backup_root}"')
    print("=" * 80)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Enterprise Safe Updater for Agentic SDLC OS")
    parser.add_argument("--target", default=".", help="Target project root directory (default: current directory)")
    parser.add_argument("--source", help="Path to upstream framework repository or local release directory")
    parser.add_argument("--dry-run", action="store_true", help="Inspect planned changes without writing to disk")
    parser.add_argument("--skip-validation", action="store_true", help="Skip running post-update verification tests")
    parser.add_argument("--rollback", help="Path to a backup directory to restore from")
    args = parser.parse_args()

    target_root = Path(args.target).resolve()

    if args.rollback:
        success = rollback(args.rollback, target_root)
        sys.exit(0 if success else 1)

    # Resolve source
    is_temp = False
    source_path = None
    if args.source:
        source_path = Path(args.source).resolve()
    else:
        # Check if local repo is framework source root
        script_dir = Path(__file__).resolve().parent
        framework_candidate = script_dir.parent
        if (framework_candidate / "plugin.json").exists() and (framework_candidate / ".agents").exists():
            source_path = framework_candidate
        else:
            # Clone shallow from GitHub
            import tempfile
            temp_dir = Path(tempfile.mkdtemp(prefix="sdlc-update-"))
            print(f"[DOWNLOAD] Fetching latest framework release from {DEFAULT_REPO_URL}...")
            res = subprocess.run(["git", "clone", "--depth", "1", DEFAULT_REPO_URL, str(temp_dir)])
            if res.returncode != 0:
                print(f"[ERROR] Failed to clone framework from {DEFAULT_REPO_URL}", file=sys.stderr)
                sys.exit(1)
            source_path = temp_dir
            is_temp = True

    try:
        ret = run_update(source_path, target_root, dry_run=args.dry_run, skip_validation=args.skip_validation)
        sys.exit(ret)
    finally:
        if is_temp and source_path.exists():
            shutil.rmtree(source_path, ignore_errors=True)

if __name__ == "__main__":
    main()
