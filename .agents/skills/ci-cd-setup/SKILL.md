---
name: ci-cd-setup
description: Configures deterministic CI/CD pipelines, automated testing, quality gate checks, and immutable container builds.
---

# CI/CD Setup & Platform Pipeline Workflow

## Objective
Establish automated, reproducible continuous integration and delivery pipelines enforcing quality gates G0 through G11.

## Responsible Agents
- Lead: `platform-engineer`
- Contributors: `security-lead`, `qa-lead`

## Inputs
- Project repository root and build configurations.
- Quality gate definitions from `governance/quality_gates.json`.

## Execution Sequence
1. **Design Pipeline**: Formulate build, lint, test, security scan, gate check, and containerization stages in `.github/workflows/sdlc-gates.yml`.
2. **Configure Security Scanning**: Embed automated secret scanning (`scripts/security_check.py`) and vulnerability linters into the CI workflow.
3. **Configure Gate Validation**: Include automated gate verification commands in the CI workflow.
4. **Build Container**: Verify Dockerfile builds cleanly with non-root user and minimal image size.
5. **Local CI Dry Run**: Test the pipeline scripts locally to ensure deterministic execution.

## Completion Criteria
- CI/CD workflow defined and verified.
- Automated gate checks integrated.
- Pipeline passes cleanly on local dry-run.
