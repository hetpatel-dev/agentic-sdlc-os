#!/usr/bin/env python3
"""
mcp_gate_server.py - Model Context Protocol (MCP) Stdio Server
Exposes automated gate validation operations directly to Antigravity agents.
"""

import json
import subprocess
import sys
from pathlib import Path

GATES_DEF_PATH = Path("governance/quality_gates.json")

def load_gates():
    if not GATES_DEF_PATH.exists():
        return {}
    with open(GATES_DEF_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f).get("gates", {})

TOOLS = [
    {
        "name": "get_gate_criteria",
        "description": "Retrieves the required criteria, artifacts, and approvers for a quality gate (G0 to G11).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "gate": {"type": "string", "description": "Gate ID (e.g. G0, G1, G2...)"}
            },
            "required": ["gate"]
        }
    },
    {
        "name": "validate_gate",
        "description": "Runs automated gate validation checks for a specified task and gate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "gate": {"type": "string", "description": "Gate ID to validate (e.g. G1)"},
                "task_id": {"type": "string", "description": "The task ID to validate"}
            },
            "required": ["gate", "task_id"]
        }
    }
]

def handle_tool_call(name, arguments):
    if name == "get_gate_criteria":
        gate_id = arguments.get("gate", "").upper()
        gates = load_gates()
        gate = gates.get(gate_id)
        if not gate:
            return f"Gate '{gate_id}' not found. Available gates: {list(gates.keys())}"
        return json.dumps(gate, indent=2)

    elif name == "validate_gate":
        gate_id = arguments.get("gate", "").upper()
        task_id = arguments.get("task_id", "")
        cmd = [sys.executable, "scripts/gate_validator.py", "--gate", gate_id, "--task", task_id]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return (res.stdout + "\n" + res.stderr).strip()

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
                        "name": "sdlc-gate-validator",
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
