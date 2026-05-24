# Doggy Dog Diary — Design

This document captures the detailed design resolved during domain review. Domain language lives in [CONTEXT.md](../CONTEXT.md); the phased build plan in [design_plan.md](design_plan.md); architectural decisions in [docs/adr/](adr/).

## Goals

- Household-scale pet diary: a handful of dogs, durable record-keeping
- No cloud hosting — each family device runs a local **Instance**
- Multiple family members contribute data via **Sync packets** (manual in v1)
- Minimal stack: TypeScript SPA + Python FastAPI + SQLite

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Browser  →  localhost:8000                             │
├─────────────────────────────────────────────────────────┤
│  FastAPI (single process)                               │
│    ├── REST API                                         │
│    ├── Static SPA (built frontend)                      │
│    ├── SQLite  (diary.db)                               │
│    └── photos/  (profile photos, augmented local copies)│
├─────────────────────────────────────────────────────────┤
│  config.yaml  →  storage_path, instance_id, host, port  │
└─────────────────────────────────────────────────────────┘

     Sync (v1 manual):  Instance A  ──ZIP──▶  Instance B
```

| Layer | Technology |
|-------|------------|
| Frontend | TypeScript, Tailwind CSS, SPA with client-side routing |
| Backend | Python 3.14, FastAPI |
| Persistence | SQLite + filesystem ([ADR 0001](adr/0001-sqlite-and-filesystem-persistence.md)) |
| Sync | Incremental ZIP export/import ([ADR 0003](adr/0003-peer-instances-file-sync.md)) |

## Domain model

### Core entities

```
Household (implicit, single)
├── Dogs[]
│   ├── Profile (structured fields + description + profile photo)
│   ├── Medication regimens[]
│   └── Events[] (via participation)
├── Tags[] (household-scoped)
└── Instances[] (physical devices, identified by instance_id in config)

Event
├── id (UUID), occurred_at, created_at, updated_at
├── notes (optional), tags[]
├── participants: Dog[] (1 for most; N for walks)
├── parent_id (optional → Parent Event)
├── measurements[] (typed key-value)
└── photo_references[] (phase 2; profile photo separate)

Medication regimen
├── id (UUID), dog_id, drug_name, dose, frequency
├── start_date, end_date (null = active)
└── notes, created_at, updated_at
```

### Key rules

1. **Profile** is a living document — not a chronological stream.
2. **Events** are the atomic diary unit. **Measurements** are chartable facts on Events. **Tags** are cross-cutting labels.
3. **Views** are query lenses + entry templates, not storage partitions.
4. **Walks** are multi-dog parent Events with `distance_miles`; child Events (e.g. pooh) link via `parent_id`.
5. **Medication regimens** track current/past prescriptions; dose Events deferred.

### Profile fields (v1)

| Field | Type |
|-------|------|
| Name | text, required |
| Date of birth | date, optional |
| Sex | male / female / unknown |
| Breed | text, optional |
| Neutered/spayed | boolean, optional |
| Microchip number | text, optional |
| Dog status | current / deceased / rehomed |
| Status date | date, optional |
| Kennel club registration | registered name, number, registering body — all optional |
| Description | free-form text, mutable |

### v1 Views and measurements

| View | Entry template | Query | Chart |
|------|----------------|-------|-------|
| Weight | date + `weight_lb` + notes/tags | Events with `weight_lb` | Line (lb over time) |
| Pooh | date + `pooh_size` (small/medium/large) + notes/tags | Events with `pooh_size` | Count or size over time |
| Walks | date + participating dogs + `distance_miles` + notes/tags; optional child events | Events with `distance_miles` | Miles over time |
| Health | date + notes/tags (no required measurements) | Events tagged `health` OR health-related tags | Timeline |
| Medicines | regimen form (not Event-based) | Active + past regimens for dog | Regimen timeline |
| Miscellaneous | date + notes/tags only | Events with no structured measurements (or explicit misc flag) | Timeline |

**Deferred:** Training, Certificates, Photos gallery, pooh consistency, dose Events, album augmentation.

### Dog status UX

- Current dogs sort first on home screen; non-current dogs follow with a visual indicator (e.g. memorial ribbon).
- All history, search, charts, and export include non-current dogs.

## UI structure

Hybrid navigation ([CONTEXT.md](../CONTEXT.md#ui-conventions)):

| Screen | Route (illustrative) | Notes |
|--------|----------------------|-------|
| Home | `/` | Dog tiles, current first |
| Dog detail | `/dogs/:id` | Profile summary, View icons, active meds |
| View list | `/dogs/:id/:view` | e.g. weight, pooh, walks |
| Event detail | `/dogs/:id/events/:eventId` | Jump target from search |
| Search | `/search` | Tag filter + optional text |
| Sync | `/sync` | Export/import sync packets |
| Charts | embedded in View screens | Per-view + cross-dog comparison (phase 2 polish) |

Quick-create overlays (modals): log weight, log pooh, log walk, add misc note, edit profile field.

## Data model (SQLite)

All tables include `id` (UUID text), `created_at`, `updated_at` unless noted.

```
dogs
  id, name, date_of_birth, sex, breed, neutered, microchip,
  status, status_date,
  kc_registered_name, kc_number, kc_body,
  description, profile_photo_path

tags
  id, name  (unique per household)

events
  id, occurred_at, notes, parent_id (nullable FK events)

event_dogs           -- many-to-many participation
  event_id, dog_id

event_tags
  event_id, tag_id

measurements
  id, event_id, type, value_json
  -- type examples: weight_lb, pooh_size, distance_miles
  -- value_json: number or string enum

medication_regimens
  id, dog_id, drug_name, dose, frequency,
  start_date, end_date, notes

photo_references     -- phase 2
  id, event_id (nullable), dog_id (nullable),
  external_url, album_url, local_copy_path, augmented_at

sync_state           -- tracks last successful import/export per peer
  id, peer_instance_id, last_sync_at
```

Indexes: `events.occurred_at`, `measurements(event_id, type)`, `events.parent_id`, full-text on `events.notes` and `dogs.description` (SQLite FTS5).

## API outline

REST JSON under `/api/v1/`:

| Area | Endpoints |
|------|-----------|
| Dogs | `GET/POST /dogs`, `GET/PATCH /dogs/:id`, profile photo upload |
| Events | `GET/POST /dogs/:id/events`, `GET/PATCH/DELETE /events/:id` |
| Walks | `POST /walks` (multi-dog + distance), `POST /events/:id/children` |
| Measurements | embedded in Event create/update payloads |
| Regimens | `GET/POST /dogs/:id/regimens`, `PATCH /regimens/:id` |
| Tags | `GET/POST /tags` |
| Views | `GET /dogs/:id/views/:viewKey}` — server-side query + chart data |
| Search | `GET /search?tags=&q=&dog_id=` |
| Export | `POST /export/full`, `POST /export/dog/:id`, `POST /export/sync?since=` |
| Import | `POST /import/sync` (merge), `POST /import/restore` (full replace, backup use) |

Static files: `GET /*` → SPA fallback.

## Sync protocol

Sync packets are ZIP files ([ADR 0002](adr/0002-export-as-zip-archive.md)) with manifest:

```json
{
  "format_version": 1,
  "export_type": "sync",
  "source_instance_id": "...",
  "exported_at": "ISO8601",
  "since_timestamp": "ISO8601",
  "dogs": [...],
  "events": [...],
  "measurements": [...],
  "regimens": [...],
  "tags": [...]
}
```

**Merge rules** ([ADR 0003](adr/0003-peer-instances-file-sync.md)):

| Record type | Rule |
|-------------|------|
| New Event (unknown UUID) | Insert |
| Existing Event | Last-write-wins on `updated_at` |
| Profile, regimen, tag | Last-write-wins on `updated_at` |
| New tag name | Insert (union) |
| Local photo assets | Copy into `photos/` if not present (by asset UUID) |

Import response includes a merge summary: added/updated/skipped counts.

**v1 transport:** User exports sync ZIP, transfers manually (AirDrop, shared folder, USB), imports on other Instance.

**Phase 2:** Watched-folder auto-import/export.

## Photos (phase 2 design, captured now)

| Asset | Storage |
|-------|---------|
| Profile photo | Always local |
| Gallery / event photos | External URL default; optional local copy via augment |
| Album | Bookmark in v1 of photos phase; import-on-augment later |

## Search

Tag-primary, optional text filter ([CONTEXT.md](../CONTEXT.md)):

- Filter by one or more tags, optional dog, optional text substring (notes, descriptions, drug names)
- Each result links to source Event, regimen, or dog profile

## Charts

- **Single dog, single metric:** line or bar from measurements over date range
- **Same metric, multiple dogs:** overlay on one chart (brief requirement)
- **Different metrics, same dog(s):** dual axis or normalization — implementation detail, phase 2 polish
- Walks: miles over time; pooh: event count or size enum mapped to ordinal

## Configuration (YAML)

```yaml
storage_path: ~/DoggyDogDiary/data
instance_id: steve-macbook-2026      # UUID or stable string
host: 127.0.0.1                      # bind address
port: 8000
# phase 2:
# sync_watch_folder: ~/iCloud/DoggyDogDiary/sync
```

## Export (backup)

Full export: entire household ZIP (same format as sync but `export_type: full`, no `since` filter).

Single-dog export: filtered manifest + shared walk Events where dog participated.

## Non-goals (v1)

- Authentication / user accounts
- Cloud hosting or always-on server
- Real-time sync
- External photo album API integration
- Dose-level medication logging
- Training, Certificates, Photos gallery Views

## Open implementation details

These are deliberate deferrals, not unresolved domain questions:

- Chart dual-axis strategy for mixed metrics
- Health view: default tag set vs free-form only
- SQLite FTS vs LIKE for text search at household scale (FTS preferred)
- Frontend framework choice (React, Vue, etc.) — pick on implementation start
- Python packaging (`uv`, `pip`, single binary via PyInstaller — defer)
