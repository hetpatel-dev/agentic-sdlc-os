#!/usr/bin/env python3
"""
Hook adapter for Antigravity hook runner.
Outputs required JSON decision on stdout.
"""
import json
import sys

def main():
    try:
        # Read hook payload from stdin if available
        raw = sys.stdin.read()
        if raw.strip():
            payload = json.loads(raw)
    except Exception:
        pass

    # Emit required JSON output for Antigravity hook
    resp = {"decision": "allow"}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()
    sys.exit(0)

if __name__ == "__main__":
    main()
