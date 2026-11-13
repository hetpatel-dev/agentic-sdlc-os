#!/usr/bin/env python3
"""
mcp_traceability_server.py - Model Context Protocol (MCP) Stdio Server
Exposes traceability ledger queries and mutations directly to Antigravity agents.
"""

import json
import sys
from pathlib import Path

LEDGER_PATH = Path("governance/traceability_ledger.json")

def load_ledger():
    if not LEDGER_PATH.exists():
        return {"version": "1.0.0", "tasks": {}, "requirements": {}, "adrs": {}}
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ledger(data):
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

TOOLS = [
    {
        "name": "get_task_status",
        "description": "Retrieves current status, gate, and traceability links for a specific task ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The task ID (e.g. TASK-101)"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "list_tasks",
        "description": "Lists all registered tasks across SDLC domains with their current gates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Filter by domain (optional)"}
            }
        }
    },
    {
        "name": "link_artifact",
        "description": "Links an artifact (file path or commit hash) to an active task.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The task ID"},
                "artifact_path": {"type": "string", "description": "Path to deliverable artifact"}
            },
            "required": ["task_id", "artifact_path"]
        }
    }
]

def handle_tool_call(name, arguments):
    ledger = load_ledger()
    if name == "get_task_status":
        tid = arguments.get("task_id")
        task = ledger.get("tasks", {}).get(tid)
        if not task:
            return f"Task {tid} not found."
        return json.dumps(task, indent=2)

    elif name == "list_tasks":
        domain_filter = arguments.get("domain")
        tasks = ledger.get("tasks", {})
        res = []
        for tid, t in tasks.items():
            if domain_filter and t.get("domain") != domain_filter:
                continue
            res.append(f"{tid}: {t.get('title')} [{t.get('domain')}] - Gate: {t.get('current_gate')} (Status: {t.get('status')})")
        return "\n".join(res) if res else "No tasks found."

    elif name == "link_artifact":
        tid = arguments.get("task_id")
        art = arguments.get("artifact_path")
        task = ledger.get("tasks", {}).get(tid)
        if not task:
            return f"Task {tid} not found."
        if art not in task.get("artifacts", []):
            task.setdefault("artifacts", []).append(art)
            save_ledger(ledger)
            return f"Artifact {art} successfully linked to {tid}."
        return f"Artifact {art} already linked to {tid}."

    return f"Unknown tool '{name}'."

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "sdlc-traceability",
                        "version": "1.0.0"
                    }
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            pass

        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": TOOLS
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})
            result_text = handle_tool_call(name, args)
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": str(result_text)
                        }
                    ]
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif msg_id is not None:
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Method {method} not found"
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
