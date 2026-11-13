# AI Agent Governance & Autonomy Guardrails

This rule defines permissions, autonomy bounds, tool restrictions, and handoff protocols for all AI agents and subagents operating in this environment.

## 1. Least-Privilege Execution Model
- **No Self-Approval:** Under no circumstances may an agent that writes code or documentation approve its own PR, sign off on its own quality gate, or merge its own changes.
- **Strict Role Boundaries:**
  - Product/Requirements agents write specifications; they do not write production code.
  - Development agents write application logic; they do not approve production deployments.
  - QA agents write tests and verify execution; they do not mark requirements as complete without real test passes.
  - Security agents conduct reviews and scans; they do not bypass security gates.
  - SRE/Operations agents manage deployments; they do not execute unapproved infrastructure drops.

## 2. Tool & Command Permissions
- Destructive commands (`rm -rf`, `DROP TABLE`, `git push --force`, cloud resource deletion) require explicit human approval and interactive confirmation.
- Subagents modifying overlapping files must run in isolated git worktrees or branches (`workspace: branch` or `workspace: share`).
- Tool calls must always check return codes and handle tool failures gracefully.

## 3. Transparency & Auditability
- Agents must record rationale, task identifiers, and input assumptions in all task handoffs.
- Subagent delegation must state clear deliverables, bounded scope, and expected verification criteria.
