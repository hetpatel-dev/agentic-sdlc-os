# Database & Migration Safety Standards

This rule governs persistence schema changes, data migrations, zero-downtime evolution, and data integrity.

## 1. Migration Discipline
- All schema modifications (tables, columns, indexes, constraints, triggers) must be version-controlled in ordered migration files.
- Manual or out-of-band schema changes directly in production or staging environments are strictly forbidden.
- Every migration must be tested both forward (`up`) and backward (`down` / rollback) before deployment.

## 2. Zero-Downtime Expansion & Contraction
- Schema changes in production must support phased zero-downtime deployments:
  1. **Phase 1 (Expand):** Add nullable columns or new tables; deploy updated code that writes to both old and new.
  2. **Phase 2 (Backfill):** Backfill historical data in bounded batches without locking tables.
  3. **Phase 3 (Switch):** Deploy code reading from the new structure.
  4. **Phase 4 (Contract):** Remove legacy columns or tables in a subsequent release after verifying stability.
- Renaming columns directly on live databases is prohibited; use view aliasing or duplicate columns.

## 3. Query Performance & Locking
- All foreign keys must have corresponding indexes.
- Migrations adding indexes on large tables must use non-blocking creation mechanisms (e.g., `CREATE INDEX CONCURRENTLY` in PostgreSQL).
- Long-running transactions that acquire exclusive table locks must specify statement timeouts.
