# Doggy Dog Diary — Project Brief

## Purpose

Doggy Dog Diary is a personal app for tracking a small number of pet dogs and their ongoing history — health events, milestones, daily notes, and anything else worth remembering over time.

## Overview

A **single-page application** built for a household-scale use case: a handful of dogs, not a multi-tenant platform. The focus is on simple, durable record-keeping rather than social features or large-scale data management.

## Architecture

| Layer    | Stack                                      |
| -------- | ------------------------------------------ |
| Frontend | TypeScript, Tailwind CSS (lightweight SPA) |
| Backend  | Python 3.14, FastAPI                       |

The frontend is a single-page app that talks to a FastAPI backend. Both layers should stay minimal and easy to maintain.

## User Interface

### Front page

The home screen displays a **tile for each dog**. Each tile shows:

- The dog’s **name**
- A **photo** of the dog

Tiles are the primary entry point for selecting a dog and viewing or adding to their history.

### Dog detail

Clicking a tile opens either a **modal dialog** or a **dedicated view** (to be decided during implementation) showing detailed information for that dog.

#### Profile fields

- **Free-form text** — general notes or description
- **Fixed fields** — structured data such as:
  - Date of birth
  - Sex
  - Additional fields to be refined later

#### Category icons

The detail view includes icons that link to deeper, category-specific history:

| Category         | Examples of tracked data                        |
| ---------------- | ----------------------------------------------- |
| Medicines        | Current and past medications                    |
| Weight history   | Weight over time                                |
| Pooh history     | Stool / bowel movement notes                    |
| Health           | Vet visits, conditions, etc.                    |
| Exercise history | Walks, runs, activity levels over time          |
| Training         | Commands learned, sessions, progress notes      |
| Certificates     | Kennel club, obedience, health certs, etc.      |
| Photos           | Links to picture galleries or individual photos |
| *Others TBD*     | Additional categories may be added later        |

Each category opens its own detailed view for viewing and recording entries in that area.

### History entries

Individual history records — weight readings, pooh observations, exercise sessions, medicine doses, and similar **data points** — each support an **optional free-form notes** field. Structured fields capture the measurable or categorical data; notes allow extra context (e.g. “weighed after breakfast”, “unusual consistency”) without forcing everything into fixed columns.

Notes (and other free-form text where applicable) can be **tagged** with one or more labels from a **user-defined tag set** — e.g. “vet”, “diet change”, “concern”. Tags are managed by the user rather than fixed in the app.

### Tags & search

A **search** feature surfaces notes matching selected tags (and potentially other criteria to be defined). Results show the note text, which dog it belongs to, and when it was recorded.

When a note is attached to a **history data point**, search results must make it **easy to jump to that source record** — the weight entry, pooh observation, vet visit, etc. — not just display the note in isolation.

Profile-level free-form text may also support tags and appear in search; navigation from those results depends on context (e.g. open the dog’s profile).

### History charts

History categories with dated entries should support **charts over time** — plotting values or events against date. For example, **weight history** should include a weight chart showing changes over months or years.

Where a category has numeric or countable data tied to dates (weight, exercise duration, etc.), a chart view should be available alongside the raw entry list. Categories that are primarily textual or event-based (health notes, training milestones) may use a timeline rather than a numeric chart.

Charts support two kinds of comparison:

1. **Same aspect, multiple dogs** — e.g. weight for two dogs overlaid on a single graph. The user selects which dogs and which metric to include.
2. **Different aspects, same dog(s)** — e.g. weight and poo count on one chart to spot correlations over time. The user selects which metrics to overlay; how mixed units are scaled (dual axes, normalization, etc.) is an implementation detail to be decided.

## Backend & Persistence

**All application data is persisted on the backend.** The frontend reads and writes via the API; nothing important lives only in browser storage.

Runtime parameters for the backend are loaded from a **YAML config file** at startup. This includes operational settings such as:

- **Storage location** — where persistent data (database files, uploads, etc.) is kept on disk
- Other backend settings as needed (to be defined)

This keeps deployment flexible: the same codebase can target different environments or machines by swapping the config file.

### Data export

Data should be **readily exportable** from the backend:

- **All dogs** — full export of every dog and their histories
- **Individual dog** — export for a single dog only

Export supports backup, migration, and sharing records outside the app. Export format and packaging (e.g. JSON, archive with photos) to be defined.

## Open Questions

The following are not yet decided:

| Area              | Questions                                                                 |
| ----------------- | ------------------------------------------------------------------------- |
| UI                | Modal dialog vs dedicated view for dog detail                             |
| Profile           | Complete list of fixed profile fields                                     |
| Photos            | Stored uploads vs links to external galleries                             |
| Tags & search     | Tag scope (global vs per-dog); search scope and full-text vs tags only    |
| Data              | Storage technology and schema (SQLite, files, etc.)                       |
| Config            | Full set of YAML config parameters                                        |
| Export            | Format and whether photos are included inline or as references            |
| Operations        | Authentication, deployment, hosting                                       |
| Non-functional    | Performance, accessibility, and other quality targets                     |
