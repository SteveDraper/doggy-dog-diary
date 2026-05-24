# Doggy Dog Diary — Design Plan

Phased implementation plan for Doggy Dog Diary. Domain language is in [CONTEXT.md](../CONTEXT.md); detailed technical design in [design.md](design.md); architectural decisions in [adr/](adr/).

## Overview

The app is a local-first household pet diary. Each family device runs an independent **Instance** (single FastAPI process + SQLite + photo store). Phases 0–3 deliver a complete diary on one device; **Phase 4** adds manual sync between Instances; later phases add chart polish, photos, and automation.

### v1 scope (locked)

| View | Measurement / data |
|------|-------------------|
| Weight | `weight_lb` |
| Pooh | `pooh_size` (small / medium / large) |
| Walks | `distance_miles`; multi-dog parent Events |
| Health | Tag-driven timeline (no required measurements) |
| Medicines | Medication regimens |
| Miscellaneous | Notes + tags only |

Deferred beyond initial Views: Training, Certificates, Photos gallery, pooh consistency, dose Events.

---

## Phase 0 — Project skeleton

**Goal:** Runnable empty app; dev workflow established.

- [ ] Repo layout: `backend/`, `frontend/`, `docs/`, config example
- [ ] FastAPI app serving health check + static SPA placeholder
- [ ] TypeScript + Tailwind SPA scaffold with client-side router
- [ ] YAML config loading (`storage_path`, `instance_id`, `host`, `port`)
- [ ] SQLite connection; Alembic or lightweight migration setup
- [ ] Single command: `doggy-dog-diary start` (or `make run`)
- [ ] Dev mode: Vite proxy to API

**Done when:** `localhost:8000` shows placeholder home; config creates data directory.

---

## Phase 1 — Dogs and profiles

**Goal:** Home screen with dog tiles; create and edit profiles.

- [ ] `dogs` table + migrations
- [ ] CRUD API for dogs
- [ ] Profile photo upload (local storage only)
- [ ] Home screen: tiles (name + photo), current dogs first
- [ ] Dog detail screen (profile fields, description, status indicator)
- [ ] Quick-edit overlay for profile fields
- [ ] Kennel club registration fields (registered name, number, registering body)

**Done when:** Add Nico and Bella, upload photos, set status, edit description.

---

## Phase 2 — Events, measurements, and Views

**Goal:** Core diary logging for weight, pooh, walks, misc.

- [ ] `events`, `event_dogs`, `measurements`, `tags`, `event_tags` tables
- [ ] Event CRUD API with UUID + `created_at` / `updated_at`
- [ ] Tag management (household-scoped)
- [ ] **Weight view:** log `weight_lb`, list, basic line chart
- [ ] **Pooh view:** log `pooh_size` (small / medium / large), list, chart
- [ ] **Walk view:** multi-dog parent Event + `distance_miles`, list, chart
- [ ] **Child Events:** record pooh during walk (parent link)
- [ ] **Miscellaneous view:** notes + tags only
- [ ] View icons on dog detail → View screens
- [ ] Event detail screen

**Done when:** Full walk + mid-walk pooh scenario works; weight and pooh histories chart correctly.

---

## Phase 3 — Health view, medicines, search

**Goal:** Cross-cutting concerns and findability.

- [ ] **Health view:** query Events by health-related tags; timeline display
- [ ] `medication_regimens` table + API
- [ ] Medicines section on dog detail (active regimens); regimen history
- [ ] **Search screen:** tag filter (primary) + optional text + optional dog filter
- [ ] Search results jump to Event, regimen, or profile
- [ ] Profile description included in search index

**Done when:** Tag a pooh Event `#health` → appears in Health view and search; manage Apoquel regimen.

---

## Phase 4 — Export, import, and sync

**Goal:** Multi-Instance household via manual sync packets.

- [ ] Full export ZIP (JSON manifest + `photos/`)
- [ ] Single-dog export ZIP
- [ ] Incremental sync export (`since` timestamp)
- [ ] Sync import with merge rules (Event union by UUID; last-write-wins elsewhere)
- [ ] Merge summary UI
- [ ] `sync_state` tracking (last sync per peer `instance_id`)
- [ ] Sync screen: export sync / import sync / full backup export

**Done when:** Two Instances exchange a sync packet; Events and profile changes appear on both; merge summary shown.

---

## Phase 5 — Charts and polish

**Goal:** Comparison charts and UX refinement from the project brief.

- [ ] Multi-dog overlay chart (same metric, e.g. `weight_lb`)
- [ ] Mixed-metric chart (dual axis or normalized) — pick strategy during implementation
- [ ] Dog comparison selector on chart screens
- [ ] Memorial / status visual treatment on home-screen tiles
- [ ] Empty states, validation, error handling
- [ ] Basic accessibility pass (keyboard navigation, labels)

**Done when:** Compare Nico and Bella weight on one chart; non-current dog tile visually distinct.

---

## Phase 6 — Photos gallery

**Goal:** Photo references and hybrid storage model.

- [ ] `photo_references` table
- [ ] **Photos view:** external URL default; single-photo augment to local copy
- [ ] Album bookmark (link out; no inline gallery in v1 of this phase)
- [ ] Photo attachments on Events
- [ ] Include photo references + local copies in export / sync

**Done when:** Link external photo to Event; augment to local copy; survives in sync packet.

---

## Phase 7 — Automation and extended Views

**Goal:** Reduce sync friction; complete category coverage.

- [ ] Watched-folder auto sync (iCloud / shared directory)
- [ ] **Training view** (timeline + notes / tags)
- [ ] **Certificates view** (structured fields TBD)
- [ ] Album-wide augment (import-on-augment)
- [ ] Dose Events (optional medication logging)
- [ ] Pooh consistency measurement
- [ ] Full import / restore (replace database from backup ZIP)

---

## Build order rationale

```
Phase 0–1   Foundation + dogs        ← see something on screen fast
Phase 2     Events (daily use)       ← core value without sync
Phase 3     Meds + search            ← complete single-Instance usefulness
Phase 4     Sync                     ← unlock multi-device household
Phase 5     Charts polish            ← nice-to-have on working data
Phase 6–7   Photos + automation      ← larger scope, depends on stable core
```

Phases 0–3 deliver a **complete single-Instance diary**. Phase 4 is the inflection point for the multi-device requirement. Phases 5–7 are incremental enrichment.

---

## Testing strategy

- **Backend:** pytest for merge logic, export / import round-trip, View queries, sync conflict (last-write-wins)
- **Frontend:** manual household scenarios as checklist per phase
- **Sync:** scripted two-database merge tests with fixture ZIPs

---

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Sync merge bugs | Extensive pytest fixtures; merge summary surfaces unexpected overwrites |
| Last-write-wins profile clobber | Rare in practice; Phase 7 could add primary-device override if needed |
| Photo augment provider auth | External links only initially; augment best-effort with clear failure message |
| Scope creep on Views | v1 locked to six Views; defer Training / Certificates / Photos |

---

## Related documents

| Document | Purpose |
|----------|---------|
| [project_brief.md](project_brief.md) | Original product brief |
| [design.md](design.md) | Detailed technical design (schema, API, sync protocol) |
| [CONTEXT.md](../CONTEXT.md) | Domain glossary |
| [adr/](adr/) | Architectural decision records |
