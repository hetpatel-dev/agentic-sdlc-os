#!/usr/bin/env python3
"""
security_check.py - Security & Secret Scanner for Agentic SDLC OS
Runs as pre-tool/post-tool hook and pre-commit audit to prevent secrets and dangerous actions.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# High-confidence secret patterns
SECRET_PATTERNS = [
    (r"-----BEGIN (?:RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----", "Private cryptographic key"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"(?:api[_-]?key|apikey|secret[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]", "API or Secret Key assignment"),
    (r"(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]", "Plaintext password assignment"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    (r"xox[baprs]-[0-9a-zA-Z]{10,48}", "Slack Token"),
    (r"AIza[0-9A-Za-z\\-_]{35}", "Google API Key")
]

# High-risk destructive commands
DANGEROUS_COMMANDS = [
    r"rm\s+-rf\s+(?:/|\.\.|\~|\*)",
    r"DROP\s+(?:DATABASE|SCHEMA|TABLE)\s+",
    r"git\s+push\s+.*--force\s+origin\s+(?:main|master|prod|production)",
    r"mkfs(?:\.[a-z0-9]+)?\s+",
    r"dd\s+if=.*of=/dev/[a-z]+"
]

# Ignored paths
IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".gemini"}
IGNORE_FILES = {"package-lock.json", "poetry.lock", "traceability_ledger.json"}

def scan_text_for_secrets(text, source_name="<input>"):
    findings = []
    for line_num, line in enumerate(text.splitlines(), start=1):
        if "# nosec" in line or "# allow-secret" in line:
            continue
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                # Avoid flagging self-references in security_check.py itself
                if "SECRET_PATTERNS" in line or "pattern" in line:
                    continue
                findings.append(f"{source_name}:{line_num}: Detected {desc}")
    return findings

def scan_command_for_danger(cmd):
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return f"Dangerous command blocked by safety rule: '{cmd}' matches '{pattern}'"
    return None

def scan_directory(root_dir="."):
    all_findings = []
    for path in Path(root_dir).rglob("*"):
        if path.is_file():
            parts = set(path.parts)
            if parts & IGNORE_DIRS or path.name in IGNORE_FILES:
                continue
            if path.name == "security_check.py":
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                findings = scan_text_for_secrets(content, str(path))
                all_findings.extend(findings)
            except Exception:
                pass
    return all_findings

def main():
    parser = argparse.ArgumentParser(description="Security & Secret Scanner for Agentic SDLC OS")
    parser.add_argument("--stage", choices=["pre-command", "post-write", "audit"], default="audit")
    parser.add_argument("--command", help="Command string to audit (for pre-command stage)")
    parser.add_argument("--file", help="Specific file to audit")
    args = parser.parse_args()

    if args.stage == "pre-command":
        cmd = args.command or os.environ.get("AGY_TOOL_COMMAND", "")
        if cmd:
            danger = scan_command_for_danger(cmd)
            if danger:
                print(f"[SECURITY BLOCKED] {danger}", file=sys.stderr)
                sys.exit(1)
        sys.exit(0)

    if args.stage == "post-write" and args.file:
        p = Path(args.file)
        if p.exists() and p.is_file():
            content = p.read_text(encoding="utf-8", errors="ignore")
            findings = scan_text_for_secrets(content, str(p))
            if findings:
                print(f"[SECURITY ALERT] Secrets detected in {args.file}:", file=sys.stderr)
                for f in findings:
                    print(f"  [-] {f}", file=sys.stderr)
                sys.exit(1)
        sys.exit(0)

    # Full audit
    print("[SECURITY] Running repository security and secret audit...")
    findings = scan_directory(".")
    if findings:
        print(f"[FAILED] Security scan found {len(findings)} potential secret(s):", file=sys.stderr)
        for f in findings:
            print(f"  [-] {f}", file=sys.stderr)
        sys.exit(1)
    else:
        print("[SUCCESS] Security scan clean. Zero secrets detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
