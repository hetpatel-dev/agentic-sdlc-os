#!/usr/bin/env python3
"""
traceability_cli.py - Traceability Ledger CLI for Agentic SDLC OS
Enforces bidirectional traceability from business objectives through production releases.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

LEDGER_PATH = Path("governance/traceability_ledger.json")

VALID_DOMAINS = [
    "strategy", "requirements", "architecture", "ux", "delivery",
    "development", "data", "quality", "security", "performance",
    "devops", "release", "operations", "observability", "maintenance", "governance"
]

VALID_GATES = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "CLOSED"]
VALID_STATUSES = ["PROPOSED", "IN_PROGRESS", "REVIEW", "BLOCKED", "COMPLETED", "CLOSED"]

def load_ledger():
    if not LEDGER_PATH.exists():
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0.0",
            "system": "Agentic SDLC OS",
            "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "objectives": {},
            "requirements": {},
            "adrs": {},
            "tasks": {}
        }
        save_ledger(data)
        return data
    with open(LEDGER_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save_ledger(data):
    data["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def cmd_init(args):
    ledger = load_ledger()
    print(f"[OK] Traceability ledger initialized at {LEDGER_PATH}")
    print(f"     Tasks tracked: {len(ledger.get('tasks', {}))}")
    print(f"     Requirements tracked: {len(ledger.get('requirements', {}))}")

def cmd_create_objective(args):
    ledger = load_ledger()
    obj_id = args.id
    if not obj_id:
        existing = [int(k.replace("OBJ-", "")) for k in ledger.get("objectives", {}).keys() if k.startswith("OBJ-") and k.replace("OBJ-", "").isdigit()]
        next_num = max(existing) + 1 if existing else 1
        obj_id = f"OBJ-{next_num:03d}"

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    obj = {
        "id": obj_id,
        "title": args.title,
        "status": args.status or "APPROVED",
        "created_at": now
    }
    ledger.setdefault("objectives", {})[obj_id] = obj
    save_ledger(ledger)
    print(f"[SUCCESS] Registered objective {obj_id}: {args.title}")

def cmd_create_requirement(args):
    ledger = load_ledger()
    req_id = args.id
    if not req_id:
        existing = [int(k.replace("REQ-", "")) for k in ledger.get("requirements", {}).keys() if k.startswith("REQ-") and k.replace("REQ-", "").isdigit()]
        next_num = max(existing) + 1 if existing else 1
        req_id = f"REQ-{next_num:03d}"

    req = {
        "id": req_id,
        "title": args.title,
        "objective_id": args.obj,
        "doc_path": args.doc or "",
        "status": args.status or "APPROVED"
    }
    ledger.setdefault("requirements", {})[req_id] = req
    save_ledger(ledger)
    print(f"[SUCCESS] Registered requirement {req_id}: {args.title} (Objective: {args.obj})")

def cmd_create_adr(args):
    ledger = load_ledger()
    adr_id = args.id
    if not adr_id:
        existing = []
        for k in ledger.get("adrs", {}).keys():
            cleaned = k.replace("ADR-", "")
            if cleaned.isdigit():
                existing.append(int(cleaned))
        next_num = max(existing) + 1 if existing else 1
        adr_id = f"ADR-{next_num:04d}"

    adr = {
        "id": adr_id,
        "title": args.title,
        "status": args.status or "ACCEPTED",
        "doc_path": args.doc or ""
    }
    ledger.setdefault("adrs", {})[adr_id] = adr
    save_ledger(ledger)
    print(f"[SUCCESS] Registered ADR {adr_id}: {args.title}")

def cmd_create_task(args):
    ledger = load_ledger()
    task_id = args.task_id
    if not task_id:
        existing = [int(k.replace("TASK-", "")) for k in ledger["tasks"].keys() if k.startswith("TASK-") and k.replace("TASK-", "").isdigit()]
        next_num = max(existing) + 1 if existing else 1
        task_id = f"TASK-{next_num:03d}"

    if args.domain not in VALID_DOMAINS:
        print(f"[ERROR] Invalid domain '{args.domain}'. Allowed domains: {', '.join(VALID_DOMAINS)}", file=sys.stderr)
        sys.exit(1)

    gate = args.gate or "G0"
    if gate not in VALID_GATES:
        print(f"[ERROR] Invalid gate '{gate}'. Allowed gates: {', '.join(VALID_GATES)}", file=sys.stderr)
        sys.exit(1)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    task = {
        "id": task_id,
        "title": args.title,
        "domain": args.domain,
        "status": "PROPOSED",
        "current_gate": gate,
        "created_at": now,
        "updated_at": now,
        "assigned_agent": args.agent or "sdlc-orchestrator",
        "traceability": {
            "objective_id": args.obj or "",
            "requirement_ids": [r.strip() for r in args.req.split(",") if r.strip()] if args.req else [],
            "user_story_ids": [],
            "adr_ids": [a.strip() for a in args.adr.split(",") if a.strip()] if args.adr else [],
            "commits": [],
            "test_case_ids": [],
            "release_version": ""
        },
        "artifacts": [],
        "gate_history": [],
        "risks": []
    }
    ledger["tasks"][task_id] = task
    save_ledger(ledger)
    print(f"[SUCCESS] Created task {task_id}: {args.title} (Domain: {args.domain}, Gate: {task['current_gate']})")

def cmd_update_task(args):
    ledger = load_ledger()
    task_id = args.task_id
    if task_id not in ledger["tasks"]:
        print(f"[ERROR] Task {task_id} not found in ledger.", file=sys.stderr)
        sys.exit(1)

    task = ledger["tasks"][task_id]
    if args.status:
        task["status"] = args.status
    if args.gate:
        task["current_gate"] = args.gate
    if args.agent:
        task["assigned_agent"] = args.agent
    task["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    save_ledger(ledger)
    print(f"[SUCCESS] Updated {task_id}: Status={task['status']}, Gate={task['current_gate']}, Agent={task['assigned_agent']}")

def cmd_link(args):
    ledger = load_ledger()
    task_id = args.task_id
    if task_id not in ledger["tasks"]:
        print(f"[ERROR] Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)

    task = ledger["tasks"][task_id]
    if args.artifact:
        if args.artifact not in task["artifacts"]:
            task["artifacts"].append(args.artifact)
            print(f"[LINK] Artifact added: {args.artifact} -> {task_id}")
    if args.req:
        for r in args.req.split(","):
            r = r.strip()
            if r and r not in task["traceability"]["requirement_ids"]:
                task["traceability"]["requirement_ids"].append(r)
                print(f"[LINK] Requirement linked: {r} -> {task_id}")
    if args.adr:
        for a in args.adr.split(","):
            a = a.strip()
            if a and a not in task["traceability"]["adr_ids"]:
                task["traceability"]["adr_ids"].append(a)
                print(f"[LINK] ADR linked: {a} -> {task_id}")
    if args.commit:
        if args.commit not in task["traceability"]["commits"]:
            task["traceability"]["commits"].append(args.commit)
            print(f"[LINK] Commit linked: {args.commit} -> {task_id}")
    if args.test:
        for t in args.test.split(","):
            t = t.strip()
            if t and t not in task["traceability"]["test_case_ids"]:
                task["traceability"]["test_case_ids"].append(t)
                print(f"[LINK] Test case linked: {t} -> {task_id}")

    task["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_ledger(ledger)

def cmd_record_gate(args):
    ledger = load_ledger()
    task_id = args.task_id
    if task_id not in ledger["tasks"]:
        print(f"[ERROR] Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)

    task = ledger["tasks"][task_id]
    record = {
        "gate": args.gate,
        "status": args.status.upper(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "verified_by": args.verifier,
        "evidence": args.evidence or "Automated gate check verification"
    }
    task["gate_history"].append(record)
    if args.status.upper() == "PASSED":
        # Advance gate if appropriate
        gates = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "CLOSED"]
        if args.gate in gates:
            idx = gates.index(args.gate)
            if idx + 1 < len(gates):
                task["current_gate"] = gates[idx + 1]
    task["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_ledger(ledger)
    print(f"[SUCCESS] Recorded Gate {args.gate} as {args.status.upper()} by {args.verifier} for {task_id}. Current gate: {task['current_gate']}")

def cmd_status(args):
    ledger = load_ledger()
    if args.task_id:
        task = ledger["tasks"].get(args.task_id)
        if not task:
            print(f"[ERROR] Task {args.task_id} not found.", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(task, indent=2))
        return

    print("================================================================================")
    print("                    AGENTIC SDLC OS — TASK LEDGER STATUS                         ")
    print("================================================================================")
    if not ledger["tasks"]:
        print("No tasks registered in ledger yet.")
        return

    print(f"{'TASK ID':<10} | {'DOMAIN':<14} | {'STATUS':<11} | {'GATE':<6} | {'AGENT':<22} | {'TITLE'}")
    print("-" * 88)
    for tid, t in sorted(ledger["tasks"].items()):
        print(f"{tid:<10} | {t.get('domain',''):<14} | {t.get('status',''):<11} | {t.get('current_gate',''):<6} | {t.get('assigned_agent',''):<22} | {t.get('title','')[:25]}")
    print("================================================================================")

def cmd_matrix(args):
    ledger = load_ledger()
    output_path = Path(args.output) if args.output else Path("docs/governance/traceability_matrix.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Software Factory — End-to-End Traceability Matrix",
        f"**Generated:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
        "",
        "| Task ID | Domain | Title | Objective | Requirements | ADRs | Current Gate | Status | Artifacts |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for tid, t in sorted(ledger.get("tasks", {}).items()):
        trace = t.get("traceability", {})
        obj = trace.get("objective_id", "") or "-"
        reqs = "<br>".join(trace.get("requirement_ids", [])) or "-"
        adrs = "<br>".join(trace.get("adr_ids", [])) or "-"
        artifacts = f"{len(t.get('artifacts', []))} files"
        lines.append(f"| `{tid}` | {t.get('domain','')} | {t.get('title','')} | {obj} | {reqs} | {adrs} | **{t.get('current_gate','')}** | {t.get('status','')} | {artifacts} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[SUCCESS] Traceability matrix written to {output_path}")

def cmd_check(args):
    ledger = load_ledger()
    issues = []
    
    # Check tasks
    for tid, t in ledger.get("tasks", {}).items():
        # Validate domain
        if t.get("domain") not in VALID_DOMAINS:
            issues.append(f"Task {tid}: Invalid domain '{t.get('domain')}'.")
        # Validate gate
        if t.get("current_gate") not in VALID_GATES:
            issues.append(f"Task {tid}: Invalid current_gate '{t.get('current_gate')}'.")
        # Validate status
        if t.get("status") not in VALID_STATUSES:
            issues.append(f"Task {tid}: Invalid status '{t.get('status')}'.")

        # Check artifacts exist on disk
        for art in t.get("artifacts", []):
            if not Path(art).exists():
                issues.append(f"Task {tid}: Artifact file does not exist on disk: {art}")

        # Check requirement backlinks
        trace = t.get("traceability", {})
        for req in trace.get("requirement_ids", []):
            if not req.startswith("REQ-"):
                issues.append(f"Task {tid}: Malformed requirement ID '{req}' (must start with REQ-)")
            elif ledger.get("requirements") and req not in ledger["requirements"]:
                issues.append(f"Task {tid}: Linked requirement '{req}' not registered in ledger['requirements'].")

        # Check ADR backlinks
        for adr in trace.get("adr_ids", []):
            if not adr.startswith("ADR-"):
                issues.append(f"Task {tid}: Malformed ADR ID '{adr}' (must start with ADR-)")
            elif ledger.get("adrs") and adr not in ledger["adrs"]:
                issues.append(f"Task {tid}: Linked ADR '{adr}' not registered in ledger['adrs'].")

        # Check objective backlink
        obj_id = trace.get("objective_id")
        if obj_id:
            if not obj_id.startswith("OBJ-"):
                issues.append(f"Task {tid}: Malformed objective ID '{obj_id}' (must start with OBJ-)")
            elif ledger.get("objectives") and obj_id not in ledger["objectives"]:
                issues.append(f"Task {tid}: Linked objective '{obj_id}' not registered in ledger['objectives'].")

    if issues:
        print("[WARNING] Traceability issues detected:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("[OK] Traceability ledger audit passed cleanly. All links valid.")

def main():
    parser = argparse.ArgumentParser(description="Traceability Ledger CLI for Agentic SDLC OS")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = subparsers.add_parser("init", help="Initialize or verify the traceability ledger")
    p_init.set_defaults(func=cmd_init)

    # create-objective
    p_obj = subparsers.add_parser("create-objective", help="Register a business objective")
    p_obj.add_argument("--id", required=False, help="Objective ID (e.g. OBJ-001, auto-assigned starting at 1 if omitted)")
    p_obj.add_argument("--title", required=True, help="Objective title")
    p_obj.add_argument("--status", default="APPROVED", help="Status (e.g. PROPOSED, APPROVED, COMPLETED)")
    p_obj.set_defaults(func=cmd_create_objective)

    # create-requirement
    p_req = subparsers.add_parser("create-requirement", help="Register a functional requirement")
    p_req.add_argument("--id", required=False, help="Requirement ID (e.g. REQ-001, auto-assigned starting at 1 if omitted)")
    p_req.add_argument("--title", required=True, help="Requirement title")
    p_req.add_argument("--obj", required=True, help="Parent objective ID (e.g. OBJ-001)")
    p_req.add_argument("--doc", help="Path to PRD/spec document")
    p_req.add_argument("--status", default="APPROVED", help="Status (e.g. PROPOSED, APPROVED)")
    p_req.set_defaults(func=cmd_create_requirement)

    # create-adr
    p_adr = subparsers.add_parser("create-adr", help="Register an Architecture Decision Record (ADR)")
    p_adr.add_argument("--id", required=False, help="ADR ID (e.g. ADR-0001, auto-assigned starting at 1 if omitted)")
    p_adr.add_argument("--title", required=True, help="ADR title")
    p_adr.add_argument("--doc", help="Path to ADR document")
    p_adr.add_argument("--status", default="ACCEPTED", help="Status (e.g. PROPOSED, ACCEPTED, DEPRECATED)")
    p_adr.set_defaults(func=cmd_create_adr)

    # create-task
    p_create = subparsers.add_parser("create-task", help="Create a new tracked task")
    p_create.add_argument("--title", required=True, help="Task title")
    p_create.add_argument("--domain", required=True, help="SDLC domain")
    p_create.add_argument("--task-id", help="Explicit task ID (e.g. TASK-001, auto-assigned starting at 1 if omitted)")
    p_create.add_argument("--gate", default="G0", help="Initial gate")
    p_create.add_argument("--agent", help="Assigned agent")
    p_create.add_argument("--obj", help="Objective ID")
    p_create.add_argument("--req", help="Comma-separated requirement IDs")
    p_create.add_argument("--adr", help="Comma-separated ADR IDs")
    p_create.set_defaults(func=cmd_create_task)

    # update-task
    p_update = subparsers.add_parser("update-task", help="Update task properties")
    p_update.add_argument("--task-id", required=True, help="Task ID")
    p_update.add_argument("--status", choices=["PROPOSED", "IN_PROGRESS", "REVIEW", "BLOCKED", "COMPLETED", "CLOSED"])
    p_update.add_argument("--gate", help="New gate")
    p_update.add_argument("--agent", help="New assigned agent")
    p_update.set_defaults(func=cmd_update_task)

    # link
    p_link = subparsers.add_parser("link", help="Link artifacts, reqs, commits, tests to a task")
    p_link.add_argument("--task-id", required=True, help="Task ID")
    p_link.add_argument("--artifact", help="Artifact file path")
    p_link.add_argument("--req", help="Requirement IDs (comma-separated)")
    p_link.add_argument("--adr", help="ADR IDs (comma-separated)")
    p_link.add_argument("--commit", help="Commit hash")
    p_link.add_argument("--test", help="Test case ID (comma-separated)")
    p_link.set_defaults(func=cmd_link)

    # record-gate
    p_gate = subparsers.add_parser("record-gate", help="Record a gate verification outcome")
    p_gate.add_argument("--task-id", required=True, help="Task ID")
    p_gate.add_argument("--gate", required=True, help="Gate (e.g. G0, G1, G2...)")
    p_gate.add_argument("--status", required=True, choices=["PASSED", "FAILED", "WAIVED"])
    p_gate.add_argument("--verifier", required=True, help="Agent or user who verified")
    p_gate.add_argument("--evidence", help="Evidence summary or log reference")
    p_gate.set_defaults(func=cmd_record_gate)

    # status
    p_status = subparsers.add_parser("status", help="Show task status")
    p_status.add_argument("--task-id", help="Specific task ID")
    p_status.set_defaults(func=cmd_status)

    # matrix
    p_matrix = subparsers.add_parser("matrix", help="Generate traceability matrix markdown")
    p_matrix.add_argument("--output", default="docs/governance/traceability_matrix.md", help="Output path")
    p_matrix.set_defaults(func=cmd_matrix)

    # check
    p_check = subparsers.add_parser("check", help="Audit ledger consistency")
    p_check.set_defaults(func=cmd_check)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
