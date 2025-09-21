# Maintenance

## Changelog Policy
- A `CHANGELOG.md` will be maintained with the following standard sections:
  - Added, Changed, Deprecated, Removed, Fixed, Security.

## Compatibility Policy
- Within a major version:
  - CLI commands and options remain stable.
  - Database schema changes remain backward compatible.
- Breaking changes:
  - Introduced only in major version updates.
  - Each breaking change must include:
    - Migration script (Alembic/SQL).
    - Deprecation warning period.

## Long-Term Support (LTS)
- A dedicated `release/*` branch will be maintained for stable releases.
- Hotfixes and security patches will be applied to LTS branches.

## Migration Plan
- Use Alembic for schema migrations.
- Provide scripts in `db/migrations/` for each schema change.
- Ensure backward compatibility within major versions.

## Logging & Error Handling
- All exceptions are caught and logged with user-friendly messages.
- Crash scenarios (invalid input, DB errors) are handled with graceful fallbacks.
- Logs stored in `logs/` directory for debugging.

## Testing & Deployment
- Run `pytest tests/` for unit and integration tests.
- Deployment:
  1. Install dependencies: `pip install -r requirements.txt`
  2. Initialize DB: `python start.py init-db`
  3. Run: `python start.py run`