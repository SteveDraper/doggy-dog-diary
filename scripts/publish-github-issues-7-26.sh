#!/usr/bin/env bash
# Continue publishing issues #7–#26 (after #1–#6 already exist).
set -euo pipefail

REPO="${GITHUB_REPO:-SteveDraper/doggy-dog-diary}"
GH="${GH_BIN:-gh}"

I1=1 I2=2 I3=3 I4=4 I5=5 I6=6

create_issue() {
  local title="$1" labels="$2" body="$3"
  local url
  url=$("$GH" issue create --repo "$REPO" --title "$title" --label "$labels" --body "$body")
  echo "${url##*/}"
}

I7=$(create_issue "Walk View with child Events" "afk" "$(cat <<EOF
## What to build

**Walk View** with multi-dog parent Events and child Events: log walks with participating dogs and \`distance_miles\`; record child Events (e.g. pooh mid-walk) linked via \`parent_id\`.

## Acceptance criteria

- [ ] Walk View accessible from dog detail
- [ ] Create multi-dog walk Event with \`distance_miles\`
- [ ] Walk list and miles-over-time chart work
- [ ] Child Event API links to parent walk (\`parent_id\`)
- [ ] UI records pooh (or other child Event) during a walk
- [ ] Demo scenario: walk Nico and Bella, Nico poohs mid-walk — walk detail shows both; the pooh Event for Nico appears in Pooh view

## Blocked by

- #$I4
EOF
)")
echo "  #$I7 Walk View with child Events"

I8=$(create_issue "Miscellaneous View end-to-end" "afk" "$(cat <<EOF
## What to build

**Miscellaneous View** for notes-and-tags-only Events (no required structured measurements): timeline/list display and View icon on dog detail.

## Acceptance criteria

- [ ] Miscellaneous View accessible from dog detail
- [ ] Log overlay creates Event with notes and tags only
- [ ] Timeline or list display for misc Events
- [ ] Demo scenario: add a misc note with tags; appears in Miscellaneous view

## Blocked by

- #$I4
EOF
)")
echo "  #$I8 Miscellaneous View end-to-end"

I9=$(create_issue "Health View (tag-driven timeline)" "afk" "$(cat <<EOF
## What to build

**Health View**: query Events by health-related tags (household-defined; no required default tag set) and display them as a timeline. Health-tagged Events from other Views (e.g. a pooh Event tagged health) appear here.

## Acceptance criteria

- [ ] Health View accessible from dog detail
- [ ] View queries Events matching health-related tags
- [ ] Timeline display (not a numeric chart)
- [ ] Demo scenario: tag a pooh Event \`#health\` — it appears in Health view

## Blocked by

- #$I4
EOF
)")
echo "  #$I9 Health View (tag-driven timeline)"

I10=$(create_issue "Medication regimens on dog detail" "afk" "$(cat <<EOF
## What to build

**Medication regimens** for a dog: track active and past prescriptions (drug name, dose, frequency, start/end dates, notes) on dog detail with regimen history.

## Acceptance criteria

- [ ] \`medication_regimens\` table and migrations exist
- [ ] Regimen CRUD API scoped to a dog
- [ ] Dog detail shows active regimens (no end date)
- [ ] Regimen history shows past courses
- [ ] Demo scenario: manage an Apoquel regimen with start date and optional end date

## Blocked by

- #$I4
EOF
)")
echo "  #$I10 Medication regimens on dog detail"

I11=$(create_issue "Search with tag filter and source navigation" "afk" "$(cat <<EOF
## What to build

**Search** screen: tag-primary filter with optional text and optional dog filter. Results link to the source Event, Medication regimen, or Dog Profile (not isolated snippets). Profile description is included in the search index.

## Acceptance criteria

- [ ] Search screen at \`/search\` with tag filter (primary), optional text, optional dog filter
- [ ] Results show match context (dog, date, snippet)
- [ ] Each result navigates to source Event, regimen, or Profile
- [ ] Profile description is searchable
- [ ] Demo scenario: tag a pooh Event \`#health\` — find via search and jump to Event detail

## Blocked by

- #$I4
- #$I10
EOF
)")
echo "  #$I11 Search with tag filter and source navigation"

I12=$(create_issue "Full and single-dog backup export" "afk" "$(cat <<EOF
## What to build

Backup **export** as ZIP archives: full household export and single-dog export (JSON manifest + \`photos/\`), per ADR 0002.

## Acceptance criteria

- [ ] \`POST /export/full\` produces a ZIP with JSON manifest and photos
- [ ] \`POST /export/dog/:id\` produces a filtered ZIP including shared walk Events where the dog participated
- [ ] Manifest includes \`format_version\`, \`export_type\`, \`source_instance_id\`, \`exported_at\`
- [ ] Demo scenario: export and inspect ZIP on a single Instance with dogs, Events, and regimens

## Blocked by

- #$I2
- #$I3
- #$I4
- #$I5
- #$I6
- #$I7
- #$I8
- #$I9
- #$I10
- #$I11
EOF
)")
echo "  #$I12 Full and single-dog backup export"

I13=$(create_issue "Incremental Sync packet export and merge import" "afk" "$(cat <<EOF
## What to build

**Sync packet** export and merge import: incremental export since a timestamp, merge rules (Event union by UUID; last-write-wins on \`updated_at\` elsewhere), and merge summary in the API response.

## Acceptance criteria

- [ ] \`POST /export/sync?since=\` produces incremental sync ZIP
- [ ] \`POST /import/sync\` merges into local database per sync merge rules
- [ ] New Events insert; existing Events and profiles/regimens/tags last-write-wins
- [ ] Import response includes merge summary (added / updated / skipped counts)
- [ ] pytest covers merge scenarios with fixture ZIPs
- [ ] Demo scenario: two Instances exchange a sync packet; Events and profile changes appear on both

## Blocked by

- #$I12
EOF
)")
echo "  #$I13 Incremental Sync packet export and merge import"

I14=$(create_issue "Sync screen and sync_state tracking" "afk" "$(cat <<EOF
## What to build

**Sync screen** and \`sync_state\` tracking: UI for export sync, import sync, and full backup export; track last successful sync per peer \`instance_id\`; show merge summary after import.

## Acceptance criteria

- [ ] \`sync_state\` table tracks last sync per peer \`instance_id\`
- [ ] Sync screen at \`/sync\` supports export sync, import sync, and full backup export
- [ ] Merge summary displayed in UI after import
- [ ] Demo scenario: complete manual sync workflow with visible merge summary

## Blocked by

- #$I13
EOF
)")
echo "  #$I14 Sync screen and sync_state tracking"

I15=$(create_issue "Multi-dog same-metric chart overlay" "afk" "$(cat <<EOF
## What to build

Multi-dog **comparison chart** for the same metric: dog selector on chart screens; overlay one measurement (e.g. \`weight_lb\`) for multiple selected dogs on a single chart.

## Acceptance criteria

- [ ] Chart screens include a dog comparison selector
- [ ] Same-metric overlay chart renders multiple dogs
- [ ] Demo scenario: compare Nico and Bella weight on one chart

## Blocked by

- #$I5
EOF
)")
echo "  #$I15 Multi-dog same-metric chart overlay"

I16=$(create_issue "Mixed-metric chart strategy and implementation" "hitl" "$(cat <<EOF
## What to build

Decide and implement **mixed-metric charts** for the same dog(s): overlay different measurements (e.g. weight and pooh count) using dual axis or normalization. Record the chosen strategy (ADR or design note), then implement on chart screens.

## Acceptance criteria

- [ ] Strategy decision documented (dual axis vs normalization, with rationale)
- [ ] Mixed-metric overlay available on chart screens
- [ ] User can select which metrics to compare for selected dog(s)
- [ ] Demo scenario: overlay two different metrics for one dog over the same date range

## Blocked by

- #$I15
EOF
)")
echo "  #$I16 Mixed-metric chart strategy and implementation"

I17=$(create_issue "Non-current Dog memorial treatment" "afk" "$(cat <<EOF
## What to build

Visual treatment for **non-current Dogs** (deceased, rehomed) on home-screen tiles: memorial or status indicator while keeping full history, search, and export access unchanged.

## Acceptance criteria

- [ ] Non-current dog tiles have distinct visual treatment (e.g. memorial ribbon)
- [ ] Current dogs still sort first
- [ ] History, search, charts, and export unchanged for non-current dogs
- [ ] Demo scenario: mark a dog non-current — tile is visually distinct but history remains accessible

## Blocked by

- #$I2
EOF
)")
echo "  #$I17 Non-current Dog memorial treatment"

I18=$(create_issue "Empty states, validation, and accessibility pass" "afk" "$(cat <<EOF
## What to build

UX polish across core screens: empty states, form validation, error handling, and a basic accessibility pass (keyboard navigation, labels).

## Acceptance criteria

- [ ] Empty states on View screens and search when no data matches
- [ ] Form validation with clear error messages
- [ ] API errors surfaced meaningfully in the UI
- [ ] Keyboard navigation works on primary flows
- [ ] Form inputs and interactive elements have accessible labels

## Blocked by

- #$I5
- #$I6
- #$I7
- #$I8
- #$I9
- #$I10
- #$I11
EOF
)")
echo "  #$I18 Empty states, validation, and accessibility pass"

I19=$(create_issue "Photos View with external links and single-photo augment" "afk" "$(cat <<EOF
## What to build

**Photos View** and \`photo_references\`: external URL as default for gallery/event photos; optional **local copy** via single-photo augment; album references as bookmarks (link out, no inline gallery).

## Acceptance criteria

- [ ] \`photo_references\` table and API exist
- [ ] Photos View on dog detail with external URL entries
- [ ] Single-photo augment creates a local copy in \`photos/\`
- [ ] Album reference displays metadata and links out
- [ ] Demo scenario: link external photo, augment to local copy

## Blocked by

- #$I4
EOF
)")
echo "  #$I19 Photos View with external links and single-photo augment"

I20=$(create_issue "Photo attachments on Events in export and sync" "afk" "$(cat <<EOF
## What to build

Attach **photo references** to Events; include photo references and local copies in export and sync packets.

## Acceptance criteria

- [ ] Events can have photo reference attachments
- [ ] Full export and sync packets include photo references
- [ ] Local photo copies included in ZIP \`photos/\` when present
- [ ] Demo scenario: Event with augmented photo survives export → import on another Instance

## Blocked by

- #$I19
- #$I13
EOF
)")
echo "  #$I20 Photo attachments on Events in export and sync"

I21=$(create_issue "Watched-folder auto sync" "afk" "$(cat <<EOF
## What to build

**Watched-folder auto sync**: configurable directory (e.g. iCloud shared folder) that auto-exports sync packets and auto-imports dropped packets.

## Acceptance criteria

- [ ] \`sync_watch_folder\` config parameter supported
- [ ] Export sync packet to watch folder on change (or on interval — document behavior)
- [ ] Import merge triggered when sync ZIP appears in folder
- [ ] Demo scenario: drop sync packet in watched folder; other Instance picks it up

## Blocked by

- #$I14
EOF
)")
echo "  #$I21 Watched-folder auto sync"

I22=$(create_issue "Training View" "afk" "$(cat <<EOF
## What to build

**Training View**: timeline of training-related Events with notes and tags (deferred from initial v1 Views).

## Acceptance criteria

- [ ] Training View accessible from dog detail
- [ ] Log and list training Events (notes + tags)
- [ ] Timeline display
- [ ] Demo scenario: log a training session note; appears in Training view

## Blocked by

- #$I4
EOF
)")
echo "  #$I22 Training View"

I23=$(create_issue "Certificates View" "hitl" "$(cat <<EOF
## What to build

Define structured fields for **Certificates** history (show rosettes, obedience titles, health certs, etc.), then implement the Certificates View as a timeline with those fields plus notes/tags.

## Acceptance criteria

- [ ] Structured field schema agreed and documented
- [ ] Certificates View accessible from dog detail
- [ ] Log and list certificate records
- [ ] Demo scenario: record a kennel club show result; appears in Certificates view

## Blocked by

- #$I4
EOF
)")
echo "  #$I23 Certificates View"

I24=$(create_issue "Dose Events and pooh consistency measurement" "afk" "$(cat <<EOF
## What to build

Optional **Dose Events** linked to Medication regimens, and \`pooh_consistency\` as an additional Pooh measurement (deferred from initial v1).

## Acceptance criteria

- [ ] Dose Event create/list linked to a regimen
- [ ] Pooh log supports optional consistency measurement
- [ ] Dose Events appear in regimen context or search
- [ ] Demo scenario: log a missed dose Event; log pooh with consistency note

## Blocked by

- #$I6
- #$I10
EOF
)")
echo "  #$I24 Dose Events and pooh consistency measurement"

I25=$(create_issue "Full import restore from backup ZIP" "afk" "$(cat <<EOF
## What to build

**Full import restore**: replace local database from a full backup ZIP (\`POST /import/restore\`) for disaster recovery.

## Acceptance criteria

- [ ] \`POST /import/restore\` replaces database and photos from full backup ZIP
- [ ] Confirmation/warning before destructive restore
- [ ] Demo scenario: backup Instance A, restore onto empty Instance B; data matches

## Blocked by

- #$I12
EOF
)")
echo "  #$I25 Full import restore from backup ZIP"

I26=$(create_issue "Album-wide augment (import-on-augment)" "afk" "$(cat <<EOF
## What to build

**Album-wide augment**: when augmenting an album reference, import album contents (not just single-photo augment).

## Acceptance criteria

- [ ] Album augment pulls in album contents to local storage
- [ ] Progress and failure states surfaced clearly (best-effort with clear errors)
- [ ] Demo scenario: augment a linked album; multiple photos available locally

## Blocked by

- #$I19
EOF
)")
echo "  #$I26 Album-wide augment (import-on-augment)"

echo ""
echo "Done. Created issues #$I7–#$I26"
echo "https://github.com/$REPO/issues"
