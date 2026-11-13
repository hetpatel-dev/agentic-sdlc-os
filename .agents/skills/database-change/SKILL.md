---
name: database-change
description: Governs database schema changes, zero-downtime expand/contract patterns, migration scripts, rollback tests, and query safety.
---

# Database Change & Migration Safety Workflow

## Objective
Safely evolve database schemas without service downtime, data loss, or table-locking bottlenecks.

## Responsible Agents
- Lead: `data-engineering-lead`
- Worker: `database-architect`

## Inputs
- Entity modeling requirements from architecture.
- Current schema definitions in `docs/database/`.

## Execution Sequence
1. **Design Migration**: Author sequential migration scripts (`up` and `down`).
2. **Apply Zero-Downtime Expand/Contract Rules**:
   - Adding columns: must be nullable or have safe defaults.
   - Removing columns: requires phased deployment (Phase 1: stop writing; Phase 2: stop reading; Phase 3: drop column).
3. **Verify Indexing & Locks**: Check that foreign keys are indexed and index creation is non-blocking (`CONCURRENTLY`).
4. **Test Forward and Backward**:
   - Apply migration (`up`) against test database.
   - Run rollback (`down`) and verify clean return to prior state.
   - Re-apply migration (`up`).
5. **Update ER Diagrams**: Update database documentation in `docs/database/`.

## Completion Criteria
- Reversible migration scripts created and tested.
- Rollback verified cleanly.
- Documentation updated.
