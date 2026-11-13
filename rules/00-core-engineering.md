# Universal Engineering Rules

These rules represent non-negotiable engineering standards across all disciplines, languages, and frameworks.

## 1. Absolute Integrity & Ground Truth
- **Never claim an action occurred unless verified:** Do not claim code compiled, linters succeeded, or test suites passed without actual terminal execution evidence.
- **Never hallucinate dependencies or capabilities:** Verify the presence of libraries in `package.json`, `pyproject.toml`, `go.mod`, or equivalent manifest before importing them.
- **Record all assumptions explicitly:** If a requirement or boundary condition is ambiguous, record the assumption in the task ledger and prompt for clarification rather than silently guessing.

## 2. Blast Radius & Scope Minimization
- **Strict Scope Discipline:** Only modify files directly relevant to the assigned task. Never perform unrelated cleanup or styling changes in the same commit.
- **Reversibility:** Every code change, schema update, and configuration modification must be reversible. Maintain clean diffs and modular abstractions.
- **Idempotency:** Operational scripts and data migrations must be idempotent. Re-running a command on an already updated system must not cause corruption or unexpected failure.

## 3. Security First
- **Zero Secrets in VCS:** Never commit API keys, passwords, private certificates, or environment variables containing credentials.
- **Safe Defaults:** Reject insecure configurations, wildcard CORS, unauthenticated endpoints, or disabled SSL verification in production paths.

## 4. Separation of Concerns
- **Independent Verification:** The agent writing an implementation cannot approve the implementation. A reviewer persona or human approver must validate the deliverable.
