# SQLite and filesystem for persistence

Structured data (dogs, events, measurements, tags, medication regimens) is stored in a single SQLite database. Binary assets — profile photos and augmented local copies — live on the filesystem; the database holds paths and metadata. A YAML config at startup points at a data directory containing both `diary.db` and a `photos/` folder.

DuckDB over JSON files was considered for human-readable storage and analytical queries, but rejected: this app is write-heavy (nested events, regimens, concurrent updates) and JSON-as-source-of-truth adds consistency and transaction problems without benefit at household scale. JSON remains the export format for backup and migration, not the live store.

**Considered options:** SQLite + filesystem (chosen), SQLite with BLOBs, JSON files + DuckDB query layer, DuckDB file as sole store.

**Consequences:** Backup is a directory copy. Export produces JSON plus photos. FastAPI uses standard SQLite tooling (e.g. SQLAlchemy).
