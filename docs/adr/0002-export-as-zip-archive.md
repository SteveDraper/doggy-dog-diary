# Export as ZIP archive

Exports (full household or single dog) are delivered as a ZIP file containing a JSON manifest and a `photos/` directory of included local assets. Profile photos and augmented local copies are bundled; external Photo references are preserved as URLs in the JSON.

The same ZIP format serves full backup and incremental Sync packets (records changed since a timestamp). Single-dog export includes that dog's data plus shared Events they participated in (e.g. a multi-dog walk), with other participants' exclusive data excluded.

**Considered options:** ZIP archive (chosen), JSON-only export, unzipped directory dump.

**Consequences:** Backup is one file to copy. Export mirrors the SQLite + filesystem layout in a portable, human-inspectable form.
