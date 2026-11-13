#!/usr/bin/env python3
"""
security_check.py - Security & Secret Scanner for Agentic SDLC OS
Runs as pre-tool/post-tool hook and pre-commit audit to prevent secrets and dangerous actions.
Natively implements the Antigravity hook protocol when invoked with --hook.
"""

import argparse
import json
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

# High-risk destructive commands (POSIX & Windows)
DANGEROUS_COMMANDS = [
    r"rm\s+-(?:r[fF]|[fF]r)\s+(?:/|\.\.|\~|\*)",
    r"Remove-Item\s+.*-Recurse\s+.*-Force",
    r"del\s+.*\/[sS]\s+.*\/[qQ]",
    r"rmdir\s+.*\/[sS]\s+.*\/[qQ]",
    r"format\s+[a-zA-Z]:",
    r"DROP\s+(?:DATABASE|SCHEMA|TABLE)\s+",
    r"git\s+push\s+.*--force\s+origin\s+(?:main|master|prod|production)",
    r"mkfs(?:\.[a-z0-9]+)?\s+",
    r"dd\s+if=.*of=/dev/[a-z]+"
]

# Ignored paths and extensions
IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".gemini", ".mypy_cache"}
IGNORE_FILES = {"package-lock.json", "poetry.lock", "traceability_ledger.json"}
IGNORE_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".png", ".jpg", ".jpeg", ".gif", ".ico",
    ".svg", ".exe", ".dll", ".so", ".dylib", ".bin", ".zip", ".tar",
    ".gz", ".7z", ".pdf", ".woff", ".woff2", ".ttf", ".eot"
}

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
    for root, dirs, files in os.walk(root_dir):
        # Prune ignored directories in-place so os.walk skips them entirely
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file in IGNORE_FILES:
                continue
            path = Path(root) / file
            if path.suffix.lower() in IGNORE_EXTENSIONS:
                continue
            if file == "security_check.py":
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
    parser.add_argument("--hook", action="store_true", help="Run in Antigravity hook mode (reads stdin JSON, writes stdout decision JSON)")
    args = parser.parse_args()

    # Antigravity Hook Mode
    if args.hook:
        try:
            raw = sys.stdin.read()
            payload = json.loads(raw) if raw.strip() else {}
        except Exception:
            payload = {}

        tool_call = payload.get("toolCall", {})
        tool_args = tool_call.get("args", {})

        if args.stage == "pre-command":
            cmd = tool_args.get("CommandLine") or tool_args.get("command") or args.command or os.environ.get("AGY_TOOL_COMMAND", "")
            if cmd:
                danger = scan_command_for_danger(cmd)
                if danger:
                    resp = {"decision": "deny", "reason": danger}
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
                    sys.exit(0)
            resp = {"decision": "allow"}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
            sys.exit(0)

        elif args.stage == "post-write":
            target_path = tool_args.get("Path") or args.file
            content = tool_args.get("Content")
            if target_path and not content and Path(target_path).exists():
                try:
                    content = Path(target_path).read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    content = ""
            findings = scan_text_for_secrets(content or "", target_path or "<hook>")
            if findings:
                resp = {"decision": "deny", "reason": f"Secrets detected in written content: {'; '.join(findings)}"}
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                sys.exit(0)
            sys.stdout.write(json.dumps({}) + "\n")
            sys.stdout.flush()
            sys.exit(0)

    # CLI / Pre-commit / CI Audit Mode
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
